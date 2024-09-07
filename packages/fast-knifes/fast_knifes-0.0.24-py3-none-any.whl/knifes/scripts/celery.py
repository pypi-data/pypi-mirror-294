# celery service management

import os
from os import path
import subprocess
from enum import Enum

import click

PROJECT_NAME = os.getenv("PROJECT_NAME", "")
PROJECT_DIR = os.getenv("PROJECT_DIR", "")
LOG_DIR = os.getenv("LOG_DIR", "")

CELERY_WORKER_SYSTEMD_TEMPLATE = """[Unit]
Description={NAME}.worker.service
ConditionPathExists={CELERY_PATH}
After=network.target

[Service]
WorkingDirectory={WORKING_DIRECTORY}
ExecStart={CELERY_PATH} --app={NAME}.tasks worker --loglevel=INFO  --concurrency=1
ExecReload=kill -HUP $MAINPID
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target"""


CELERY_BEAT_SYSTEMD_TEMPLATE = """[Unit]
Description={NAME}.beat.service
ConditionPathExists={CELERY_PATH}
After=network.target

[Service]
WorkingDirectory={WORKING_DIRECTORY}
ExecStart={CELERY_PATH} --app={NAME}.tasks beat --loglevel=INFO
ExecReload=kill -HUP $MAINPID
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target"""


def run_command(command) -> tuple[str, str, int]:
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False, executable="/bin/bash")
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def echo_succ(content):  # 绿色
    click.echo(click.style(content, fg="green"))


def echo_err(content):  # 红色
    click.echo(click.style(content, fg="red"))


def get_service_state(service_name: str):
    state, _, _ = run_command(f"systemctl is-active {service_name}")
    return state


class CeleryService(Enum):
    WORKER = "worker"
    BEAT = "beat"

    def __str__(self):
        return self.value


def configure(service: CeleryService):
    service_name = f"{PROJECT_NAME}.{service}"
    service_path = f"/etc/systemd/system/{service_name}.service"
    if path.exists(service_path):
        echo_err(f"{service_path} already exists, delete it first if you want to reconfigure")
        return

    template = CELERY_WORKER_SYSTEMD_TEMPLATE if service == CeleryService.WORKER else CELERY_BEAT_SYSTEMD_TEMPLATE
    celery_path = path.join(PROJECT_DIR, "venv/bin/celery")
    with open(service_path, "w", encoding="utf-8") as f:
        f.write(
            template.format(
                NAME=PROJECT_NAME,
                CELERY_PATH=celery_path,
                WORKING_DIRECTORY=PROJECT_DIR,
            )
        )
    os.chmod(service_path, mode=0o755)

    output, err, code = run_command(f"systemctl daemon-reload && systemctl enable {service_name}")
    if code != 0:
        echo_err(f"failed to enable service: {err}")
        raise SystemExit
    click.echo(output)
    echo_succ(f"{service_name} enabled")


def start(service: CeleryService):
    service_name = f"{PROJECT_NAME}.{service}"
    if get_service_state(service_name) == "active":
        echo_err(f"{service_name} is already running, use reload to restart it gracefully")
        raise SystemExit

    _, err, code = run_command(f"systemctl start {service_name}")
    if code != 0:
        echo_err(err)
        raise SystemExit
    echo_succ(f"{service_name} started")


def stop(service: CeleryService):
    service_name = f"{PROJECT_NAME}.{service}"
    if get_service_state(service_name) == "inactive":
        echo_err(f"{service_name} is already stopped")
        raise SystemExit

    _, err, code = run_command(f"systemctl stop {PROJECT_NAME}")
    if code != 0:
        echo_err(err)
        raise SystemExit
    echo_succ(f"{service_name} stopped")


def reload(service: CeleryService):
    service_name = f"{PROJECT_NAME}.{service}"
    if get_service_state(service_name) == "inactive":
        echo_err(f"{service_name} is not running, use start to start it")
        raise SystemExit

    _, err, code = run_command(f"systemctl reload {service_name}")
    if code != 0:
        echo_err(err)
        raise SystemExit
    echo_succ(f"{service_name} reloaded")


def status(service: CeleryService):
    service_name = f"{PROJECT_NAME}.{service}"
    output, err, _ = run_command(f"systemctl status {service_name}")
    click.echo(output)
    echo_err(err)  # warning message


worker = click.Group(help="celery worker management")
worker.add_command(click.Command("configure", callback=lambda: configure(CeleryService.WORKER), help="configure celery worker"))
worker.add_command(click.Command("start", callback=lambda: start(CeleryService.WORKER), help="start celery worker"))
worker.add_command(click.Command("stop", callback=lambda: stop(CeleryService.WORKER), help="stop celery worker"))
worker.add_command(click.Command("reload", callback=lambda: reload(CeleryService.WORKER), help="reload celery worker gracefully"))
worker.add_command(click.Command("status", callback=lambda: status(CeleryService.WORKER), help="show celery worker status"))


beat = click.Group(help="celery beat management")
beat.add_command(click.Command("configure", callback=lambda: configure(CeleryService.BEAT), help="configure celery beat"))
beat.add_command(click.Command("start", callback=lambda: start(CeleryService.BEAT), help="start celery beat"))
beat.add_command(click.Command("stop", callback=lambda: stop(CeleryService.BEAT), help="stop celery beat"))
beat.add_command(click.Command("reload", callback=lambda: reload(CeleryService.BEAT), help="reload celery beat gracefully"))
beat.add_command(click.Command("status", callback=lambda: status(CeleryService.BEAT), help="show celery beat status"))
