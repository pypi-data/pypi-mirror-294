# deploy script for fastapi project

import os
import time
from os import path

import click

from knifes.scripts.celery import run_command, echo_err, echo_succ, PROJECT_NAME, PROJECT_DIR, LOG_DIR, get_service_state, worker, beat, reload_celery_services

GUNICORN_SYSTEMD_TEMPLATE = """[Unit]
Description={NAME}.service
ConditionPathExists={GUNICORN_PATH}
After=network.target

[Service]
WorkingDirectory={WORKING_DIRECTORY}
ExecStart={GUNICORN_PATH} -c {GUNICORN_CONF_PATH}
ExecReload=kill -HUP $MAINPID
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target"""


@click.group()
def cli():
    """deploy script for fastapi project"""
    if not PROJECT_NAME or not PROJECT_DIR or not LOG_DIR:
        echo_err("please set PROJECT_NAME, PROJECT_DIR, LOG_DIR environment variables")
        raise SystemExit


cli.add_command(worker)
cli.add_command(beat)


@cli.command()
def knifes():
    """force install latest knifes"""
    activate_path = path.join(PROJECT_DIR, "venv/bin/activate")
    cmd = f"source {activate_path} && pip install fast-knifes --index-url https://pypi.python.org/simple -U"
    output, err, _ = run_command(cmd)
    click.echo(output)
    echo_err(err)  # warning message


@cli.command()
def modules():
    """install project dependencies"""
    _install_modules()


@cli.command()
@click.argument("line_count", default=10, type=int, help="number of lines to read")
def log(line_count=10):
    """read gunicorn last log"""
    _read_last_log(line_count)


@cli.command()
def status():
    """show gunicorn status"""
    output, err, _ = run_command(f"systemctl status {PROJECT_NAME}")
    click.echo(output)
    echo_err(err)  # warning message


@cli.command()
def configure():
    """configure gunicorn service"""
    service_path = f"/etc/systemd/system/{PROJECT_NAME}.service"
    if path.exists(service_path):
        echo_err(f"{service_path} already exists, delete it first if you want to reconfigure")
        return

    with open(service_path, "w", encoding="utf-8") as f:
        f.write(
            GUNICORN_SYSTEMD_TEMPLATE.format(
                NAME=PROJECT_NAME,
                GUNICORN_PATH=path.join(PROJECT_DIR, "venv/bin/gunicorn"),
                GUNICORN_CONF_PATH=path.join(PROJECT_DIR, f"gunicorn_{PROJECT_NAME}_conf.py"),
                WORKING_DIRECTORY=PROJECT_DIR,
            )
        )
    os.chmod(service_path, mode=0o755)

    output, err, code = run_command(f"systemctl daemon-reload && systemctl enable {PROJECT_NAME}")
    if code != 0:
        echo_err(f"failed to enable service: {err}")
        raise SystemExit
    click.echo(output)
    echo_succ(f"{PROJECT_NAME} enabled")


@cli.command()
def start():
    """start gunicorn"""
    if get_service_state(PROJECT_NAME) == "active":
        echo_err(f"{PROJECT_NAME} is already running, use reload to restart it gracefully")
        raise SystemExit

    _pull_latest_code()
    _install_modules()  # install modules before starting gunicorn

    _, err, code = run_command(f"systemctl start {PROJECT_NAME}")
    if code != 0:
        echo_err(err)
        raise SystemExit
    echo_succ(f"{PROJECT_NAME} started")

    time.sleep(2)
    _read_last_log()


@cli.command()
def reload():
    """reload gunicorn gracefully"""
    if get_service_state(PROJECT_NAME) == "inactive":
        echo_err(f"{PROJECT_NAME} is not running, use start to start it")
        raise SystemExit

    _pull_latest_code()
    _install_modules()

    _, err, code = run_command(f"systemctl reload {PROJECT_NAME}")
    if code != 0:
        echo_err(err)
        raise SystemExit
    echo_succ(f"{PROJECT_NAME} reloaded")

    # read last 6 lines of log
    time.sleep(2)
    _read_last_log()

    # reload celery worker and beat
    reload_celery_services()


@cli.command()
def stop():
    """stop gunicorn"""
    if get_service_state(PROJECT_NAME) == "inactive":
        echo_err(f"{PROJECT_NAME} is already stopped")
        raise SystemExit

    _, err, code = run_command(f"systemctl stop {PROJECT_NAME}")
    if code != 0:
        echo_err(err)
        raise SystemExit
    echo_succ(f"{PROJECT_NAME} stopped")

    # read last 6 lines of log
    time.sleep(2)
    _read_last_log()


# @cli.command()
# def restart():
#     """restart gunicorn"""
#     if get_service_state(PROJECT_NAME) == "inactive":
#         echo_err(f"{PROJECT_NAME} is not running, use start to start it")
#         raise SystemExit

#     _, err, code = run_command(f"systemctl restart {PROJECT_NAME}")
#     if code != 0:
#         echo_err(err)
#         raise SystemExit
#     echo_succ(f"{PROJECT_NAME} restarted")

#     # read last 6 lines of log
#     time.sleep(2)
#     _read_last_log()


def _pull_latest_code():
    output, err, code = run_command(f"cd {PROJECT_DIR} && git pull origin main")
    if code != 0:
        echo_err(err)
        raise SystemExit
    click.echo(output)
    echo_err(err)  # warning message


def _install_modules():
    activate_path = path.join(PROJECT_DIR, "venv/bin/activate")
    requirements_path = path.join(PROJECT_DIR, "requirements.txt")
    cmd = f"source {activate_path} && pip install -r {requirements_path}"
    output, err, code = run_command(cmd)
    if code != 0:
        echo_err(f"failed to install modules: {err}")
        raise SystemExit
    click.echo(output)
    echo_err(err)  # warning message


def _read_last_log(line_count=10):
    gunicorn_log_path = path.join(LOG_DIR, "gunicorn.log")
    output, err, _ = run_command(f"tail -{line_count} {gunicorn_log_path}")
    click.echo(output)
    echo_err(err)


if __name__ == "__main__":
    cli()
