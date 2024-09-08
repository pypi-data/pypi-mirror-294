from datetime import datetime
from pathlib import Path

from pony.orm import db_session

from guangluo_project_manager.db import Projects
from guangluo_project_manager.utils import get_config


def create_project_folder(name: str) -> None:
    config = get_config()
    project_path = Path(config['base_path']) / name
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / "00__会议评审").mkdir(parents=True, exist_ok=True)
    (project_path / "01__安装部署").mkdir(parents=True, exist_ok=True)
    (project_path / "02__迁移适配").mkdir(parents=True, exist_ok=True)
    (project_path / "03__生产操作").mkdir(parents=True, exist_ok=True)
    (project_path / "04__巡检报告").mkdir(parents=True, exist_ok=True)
    (project_path / "05__优化记录").mkdir(parents=True, exist_ok=True)
    (project_path / "06__问题处理").mkdir(parents=True, exist_ok=True)
    (project_path / "07__连接方式").mkdir(parents=True, exist_ok=True)


def archived_project_folder(name: str) -> None:
    config = get_config()
    project_path = Path(config['base_path']) / name
    project_path.rename(Path(config['base_path']) / '999_archived' / name)


@db_session
def create_project(name) -> None:
    project = Projects(name=name)
    project.flush()

    create_project_folder(name)


@db_session
def archive_project(id: int) -> None:
    project = Projects.get(id=id)
    project.archived = True
    project.update_time = datetime.now()
    project.flush()

    archived_project_folder(project.name)


@db_session
def get_projects(id: int):
    return Projects.get(id=id)


@db_session
def get_all_projects():
    return Projects.select()[:]



@db_session
def get_archived_projects(archived: bool):
    return Projects.select(archived=archived)[:]
