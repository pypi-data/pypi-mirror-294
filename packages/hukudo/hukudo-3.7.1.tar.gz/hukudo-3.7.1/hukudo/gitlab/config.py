import configparser

from gitlab.config import _get_config_files, GitlabConfigParser


def list_gitlab_names() -> [str]:
    """
    Sorted list of gitlab names defined in the configuration file, **excluding** [global].
    """
    # run this to validate the config
    GitlabConfigParser()
    # Unfortunately GitlabConfigParser does not provide a list of the defined instances, so we cobble some code
    # together based on GitlabConfigParser's implementation.
    # I know, _get_config_files is private, but hey - it's better to use this than my brittle approach to the same
    # logic. ;)
    files = _get_config_files()
    config = configparser.ConfigParser()
    config.read(files, encoding='utf-8')
    return list(sorted(set(config.sections()) - {'global'}))
