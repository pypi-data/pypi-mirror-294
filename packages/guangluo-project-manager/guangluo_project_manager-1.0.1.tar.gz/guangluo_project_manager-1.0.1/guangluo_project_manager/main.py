from pathlib import Path
from typing import Optional

import typer
from pony.orm import TransactionIntegrityError
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from guangluo_project_manager.actions import project
from guangluo_project_manager.db import db
from guangluo_project_manager.utils import get_pkg_name, get_pkg_version, get_config

app = typer.Typer()


def main() -> None:
    """
    新建配置文件，初始化数据库，创建项目目录
    :return: None
    """
    # set_sql_debug(True)

    app_dir = typer.get_app_dir(get_pkg_name())
    app_dir_path = Path(app_dir)
    app_dir_path.mkdir(parents=True, exist_ok=True)
    config_path = Path(app_dir) / "config.toml"

    if not config_path.is_file():
        template_config_path = Path(__file__).parent / "template/config.toml"
        config_path.write_text(template_config_path.read_text())

    config = get_config()
    base_path = Path(config.get('base_path'))
    base_path.mkdir(parents=True, exist_ok=True)
    (base_path / "999_archived").mkdir(parents=True, exist_ok=True)

    db.bind(provider="sqlite", filename=str(base_path / "projectmanager.db"),
            create_db=True)
    db.generate_mapping(create_tables=True)


main()


def version_callback(value: bool) -> None:
    """
    Project cli's version.
    :param value: False
    :return: None
    """
    if value:
        typer.echo(f"{get_pkg_name()} Version: {get_pkg_version()}")
        raise typer.Exit()


@app.callback()
def callback(version: Annotated[
    Optional[bool], typer.Option("--version", callback=version_callback,
                                 help="Project cli's version.")] = None) -> None:
    pass


@app.command("create")
def create_project(name: str) -> None:
    """
    Create a new project.
    """
    if name == '':
        typer.echo("Project name is required.")
        exit(1)

    try:
        project.create_project(name)
    except TransactionIntegrityError:
        typer.echo(f"Project '{name}' already exists.")


@app.command("archive")
def archive_project(
        id: Annotated[int, typer.Option(help="Project ID")]) -> None:
    """
    Archive the project.
    """
    project_item = project.get_projects(id)
    if not project_item:
        typer.echo("Project not found.")
        exit(1)

    if project_item.archived:
        typer.echo(f"Project '{project_item.name}' is archived.")
        exit(1)

    archived = typer.confirm(f"Archive project '{project_item.name}'?")
    if not archived:
        typer.echo("Operation canceled.")
        exit(1)

    project.archive_project(id)


@app.command("show")
def show_project(
        archived: Annotated[str, typer.Option(help="Project ID")] = 0) -> None:
    """
    Show all projects.
    0: Show all projects.
    1: Show unarchived projects.
    2: Show archived projects.
    """
    console = Console()

    projects = None
    if archived == "0":
        projects = project.get_all_projects()
    elif archived == "1":
        projects = project.get_archived_projects(False)
    elif archived == "2":
        projects = project.get_archived_projects(True)

    if projects is None or len(projects) == 0:
        typer.echo("Do not have any projects.")
        exit(1)

    table = Table("ID", "Project Name", "Archived", "Create Time",
                  "Update Time")
    for item in projects:
        table.add_row(str(item.id), item.name, str(item.archived),
                      str(item.create_time), str(item.update_time))

    console.print(table)


@app.command("open")
def open_project(id: Annotated[int, typer.Option(help="Project ID")]) -> None:
    """
    Open the project.
    """
    project_item = project.get_projects(id)
    if not project_item:
        typer.echo("Project not found.")
        exit(1)

    if project_item.archived:
        typer.echo(f"Project '{project_item.name}' is archived.")
        exit(1)

    config = get_config()
    base_path = Path(config.get('base_path'))
    project_path = base_path / project_item.name
    typer.launch(str(project_path))
