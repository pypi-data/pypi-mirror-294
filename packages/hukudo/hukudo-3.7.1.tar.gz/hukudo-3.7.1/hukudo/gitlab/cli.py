import json

import click
import structlog

from hukudo.gitlab.api import Gitlab
from hukudo.gitlab.config import list_gitlab_names
from hukudo.gitlab import jobs

logger = structlog.get_logger()

pass_gitlab = click.make_pass_decorator(Gitlab)


@click.group()
@click.option('--name')
@click.pass_context
def gitlab(ctx, name):
    ctx.obj = Gitlab.from_ini(name)
    log = logger.bind(instance=ctx.obj)
    log.debug('instantiated')


@gitlab.command()
def list():
    for v in list_gitlab_names():
        click.echo(v)


@gitlab.command()
@pass_gitlab
def version(gitlab: Gitlab):
    click.echo(gitlab.version())


@gitlab.command(name='jobs')
@click.argument('project')
@click.option(
    '--since', type=int, default=0, help='Only return records up to given job_id.'
)
@pass_gitlab
def jobs_(gitlab: Gitlab, project, since):
    for job in gitlab.jobs_of_project(project, since_job_id=since):
        try:
            job.attributes['duration'] = jobs.get_duration(job.attributes)
        except jobs.JobDurationParseError:
            logger.debug('could not get duration', job_id=job.attributes['id'])
        print(json.dumps(job.attributes))
