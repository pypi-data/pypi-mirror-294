#!/usr/bin/env python
"""
Downloads chromedriver.
"""

import itertools
import os
import platform
import re
import stat
import subprocess
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import IO
from xml.etree import ElementTree
from zipfile import ZipFile

import requests
import structlog

from hukudo.exc import HukudoException

logger = structlog.get_logger()

ARCHITECTURES = ['linux64', 'mac64', 'mac64_m1', 'win32']
# LHS: https://docs.python.org/3/library/platform.html#platform.system
# No Mac M2 :>
PLATFORM2ARCH = {
    'Linux': 'linux64',
    'Darwin': 'mac64',
    'Windows': 'win32',
}
_ARCH = PLATFORM2ARCH[platform.system()]
DEFAULT_EXE = 'google-chrome'
if _ARCH == 'mac64':
    DEFAULT_EXE = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

try:
    cache_dir = os.environ['REQUESTS_CACHE_DIR']
    import requests_cache

    requests_cache.install_cache(cache_dir)
except KeyError:
    pass
except ModuleNotFoundError:
    logger.error(
        'REQUESTS_CACHE_DIR set, but requests-cache not installed. Try: `pip install requests-cache`'
    )
    raise


class ParseError(HukudoException):
    pass


class ChromedriverDownloadError(HukudoException):
    pass


@dataclass
class Version:
    version: str
    tuple: tuple[int]
    major: int
    url: str = None

    @classmethod
    def parse(cls, version):
        t = tuple(int(x) for x in version.split('.'))
        return cls(
            version=version,
            tuple=t,
            major=t[0],
        )

    @classmethod
    def from_re_match(cls, regex, text):
        m = re.match(regex, text)
        if m is None:
            raise ParseError(f'Could not parse version from "{text}"')
        return cls.parse(m.group(1))

    def __lt__(self, other):
        return self.tuple < other.tuple

    def __str__(self):
        return self.version


def my_chrome_version(exe=DEFAULT_EXE) -> Version:
    out = subprocess.check_output(
        [exe, '--version'], encoding='utf-8'
    )  # e.g. 'Google Chrome 100.0.4896.127 \n'
    return Version.from_re_match(r'.*?([\d.]+).*?', out)


def driver_version(chromedriver: Path):
    out = subprocess.check_output([chromedriver, '--version'], encoding='utf-8')
    return Version.from_re_match(r'ChromeDriver ([\d.]+).*?', out)


def is_matching_my_major(chromedriver: Path, browser_exe=DEFAULT_EXE):
    return my_chrome_version(browser_exe).major == driver_version(chromedriver).major


class ChromedriverRepo:
    def __init__(
        self,
        arch,
    ):
        if arch not in ARCHITECTURES:
            raise ValueError(f'Invalid architecture {arch}')
        self.arch = arch

    def _iter_versions_pre_115(
        self,
    ):
        url = 'https://chromedriver.storage.googleapis.com/'
        response = requests.get(url)
        response.raise_for_status()
        # strip default namespace https://stackoverflow.com/a/35165997/241240
        xml = re.sub(r"""\sxmlns=["'].+?["']""", '', response.text, count=1)
        root = ElementTree.fromstring(xml)
        for e in root.findall('./Contents/Key'):
            key = e.text  # e.g. "99.0.4844.17/chromedriver_linux64.zip"
            match = re.match(rf'^([\d.]+)/chromedriver_{self.arch}.zip', key)
            if match:
                v = Version.parse(match.group(1))
                v.url = url + key
                yield v

    def _iter_versions_post_115(self):
        j_plat_url = 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'
        j_response = requests.get(j_plat_url).json()
        for j_version in j_response['versions']:
            version = Version.parse(j_version['version'])
            j_downloads = j_version['downloads']
            if 'chromedriver' in j_downloads:
                for j_plat_url in j_downloads['chromedriver']:
                    if j_plat_url['platform'] == self.arch:
                        version.url = j_plat_url['url']
                        yield version

    def versions(self):
        """
        Find versions for given architecture. See ARCHITECTURES for valid values.
        """
        return list(
            sorted(
                itertools.chain(
                    self._iter_versions_pre_115(),
                    self._iter_versions_post_115(),
                )
            )
        )

    def latest_version(self, major) -> Version:
        all_versions = self.versions()
        hits = sorted(v for v in all_versions if v.major == major)
        return hits[-1]


def _find_file(filenames):
    paths = [Path(x) for x in filenames]
    for p in paths:
        if p.name == 'chromedriver':
            return str(p)


def download_zip(version: Version) -> IO[bytes]:
    log = logger.bind(version=version)
    log.info('downloading', url=version.url)
    response = requests.get(version.url)
    response.raise_for_status()
    zipfile = ZipFile(BytesIO(response.content))
    filenames = zipfile.namelist()
    hit = _find_file(filenames)
    log.info('found binary', hit=hit)
    return zipfile.open(hit)


def download_latest(target_dir: Path, force=False) -> [Version, Path]:
    if not target_dir.is_dir():
        raise ChromedriverDownloadError(f'not a directory: {target_dir}')

    repo = ChromedriverRepo(_ARCH)
    chromedriver_version = repo.latest_version(my_chrome_version().major)

    target = target_dir / f'chromedriver-{chromedriver_version}'
    if target.exists():
        if force:
            target.unlink()
        else:
            raise FileExistsError(target)

    fd = download_zip(chromedriver_version)
    target.write_bytes(fd.read())
    target.chmod(target.stat().st_mode | stat.S_IXUSR)
    return chromedriver_version, target


def download_and_symlink(target_dir: Path, force=False, skip_symlink=False):
    if target_dir is None:
        target_dir = Path.cwd()
    if not target_dir.is_dir():
        raise ChromedriverDownloadError(f'not a directory: {target_dir}')

    try:
        version, path = download_latest(target_dir, force=force)
    except FileExistsError as e:
        raise ChromedriverDownloadError(f'file exists: {e}')

    if skip_symlink is False:
        os.chdir(target_dir)
        link = Path('chromedriver')
        link.unlink(missing_ok=True)
        link.symlink_to(path.relative_to(target_dir))

    return version, path
