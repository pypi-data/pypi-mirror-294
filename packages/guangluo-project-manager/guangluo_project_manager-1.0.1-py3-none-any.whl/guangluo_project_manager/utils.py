import tomllib
from pathlib import Path

import typer


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_config():
    app_dir = typer.get_app_dir(get_pkg_name())
    app_dir_path = Path(app_dir)
    app_dir_path.mkdir(parents=True, exist_ok=True)
    config_path = Path(app_dir) / "config.toml"

    with open(config_path, 'rb') as config_file:
        config = tomllib.load(config_file)

        return config


def get_pkg_version() -> str:
    """
    获取 cli 版本
    :return: cli version
    """
    return "1.0.0"

    # pyproject_config = get_project_root() / "pyproject.toml"
    # with open(pyproject_config, 'rb') as config_file:
    #     config = tomllib.load(config_file)
    #     version = config.get('tool').get('poetry').get('version')
    #
    #     return version


def get_pkg_name() -> str:
    """
    获取 cli 名称
    :return: cli name
    """
    return "guangluo_project_manager"

    # pyproject_config = get_project_root() / "pyproject.toml"
    # with open(pyproject_config, 'rb') as config_file:
    #     config = tomllib.load(config_file)
    #     name = config.get('tool').get('poetry').get('name')
    #
    #     return name
