import click
from athenaeum.render import Render


@click.command()
@click.argument('project_name')
def render_project(project_name):
    """
    使用命令：
    poetry run render_project example

    :param project_name:
    :return:
    """
    render = Render()
    render.render_project(project_name=project_name)
