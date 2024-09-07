from collections.abc import Iterable
from datetime import timedelta

import pytest
from gitlab.v4.objects import ProjectJob

from hukudo.gitlab.api import Gitlab
from hukudo.gitlab.config import list_gitlab_names
from hukudo.gitlab.jobs import get_duration, JobDurationParseError


@pytest.fixture
def gitlab():
    """
    For this fixture to work, you need a `~/.python-gitlab.cfg` containing something like this:

        [global]
        default = git.hukudo.de
        ssl_verify = true
        timeout = 30

        [git.hukudo.de]
        url = https://git.hukudo.de/
        private_token = xxxxxxxxxxxxxxxxxxxx
        api_version = 4
    """
    return Gitlab.from_ini('git.hukudo.de')


def test_list():
    versions = list_gitlab_names()
    assert len(versions) > 0
    assert 'global' not in versions


def test_version(gitlab):
    actual = gitlab.version()
    major, minor, patch = [int(x) for x in actual.split('.')]
    assert major >= 16
    assert minor >= 0
    assert patch >= 0


def test_jobs_of_project(gitlab):
    iterable = gitlab.jobs_of_project('experiments/flutter')
    assert isinstance(iterable, Iterable)
    xs = list(iterable)
    assert len(xs) >= 8
    job = xs[0]
    assert isinstance(job, ProjectJob)
    job_id = job.attributes['id']
    assert job_id is not None
    nothing_new = gitlab.jobs_of_project('experiments/flutter', since_job_id=job_id)
    assert list(nothing_new) == []


def test_job_with_duration_happy():
    assert get_duration(
        {
            'started_at': '2022-07-19T16:13:17.374+02:00',
            'finished_at': '2022-07-19T16:14:19.374+02:00',
        }
    ) == timedelta(seconds=62)


def test_job_with_duration_error():
    with pytest.raises(JobDurationParseError):
        get_duration(
            {
                'started_at': 'not-an-iso-datetime-string',
                'finished_at': 'not-an-iso-datetime-string',
            }
        )
