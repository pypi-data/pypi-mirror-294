from typing import Iterator
import gitlab
from gitlab.v4.objects import ProjectJob


class Gitlab:
    """
    Note the use of `iterator=True` to handle pagination
    https://python-gitlab.readthedocs.io/en/stable/api-usage.html#pagination.
    """

    PAGINATION_ARGS = {'iterator': True, 'per_page': 100}

    def __init__(self, python_gitlab_instance: gitlab.Gitlab):
        self.gl: gitlab.Gitlab = python_gitlab_instance

    @classmethod
    def from_ini(cls, name):
        return cls(gitlab.Gitlab.from_config(name))

    def version(self) -> str:
        return self.gl.version()[0]

    def jobs_of_project(
        self, project_id, since_job_id: int = 0
    ) -> Iterator[ProjectJob]:
        """
        Note that project_id can also be a string like "namespace/project". :)
        """
        p = self.gl.projects.get(project_id)
        for job in p.jobs.list(**self.PAGINATION_ARGS):
            job_id = job.attributes['id']
            if job_id <= since_job_id:
                return
            assert isinstance(job, ProjectJob)
            yield job
