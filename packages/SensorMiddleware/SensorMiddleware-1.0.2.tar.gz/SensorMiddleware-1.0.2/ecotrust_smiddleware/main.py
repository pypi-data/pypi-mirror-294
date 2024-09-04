#!/usr/bin/python3
# -*- coding: utf-8 -*-
from app.aws import upload_report_to_s3_bucket
from app.core import SensorControler, CannotReadScanData, BadManifestSyntax
from app import VERSION
from rich import print # noqa
from typing import NoReturn, Union

import typer
import os
import sys
import signal

DEBUG = os.getenv('DEBUG', False)

GUNICORN_PID_PATH = '/var/run/gunicorn.pid'
DEFAULT_ROOT_PID_PATH = '/var/run/root_process.pid'

HELP = f"""
    Sensor Middleware {VERSION} \n
    Ferramenta CLI para interagir e gerenciar os scans dos sensores EcoTrust. \n 
    
"""
app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True, add_completion=False, help=HELP)
sensor_controler: Union[None, SensorControler] = None


def full_exit():
    """
        Kill main container process
    :return:
    """
    if os.path.exists(GUNICORN_PID_PATH):
        proc_pid_path = GUNICORN_PID_PATH
    else:
        proc_pid_path = DEFAULT_ROOT_PID_PATH

    try:
        with open(proc_pid_path, 'r', newline='\n') as pid:
            pid_str = pid.read()

            try:
                pid_int = int(pid_str)
            except ValueError:
                pass
            else:
                if not os.getenv('DEBUG', False):
                    os.kill(pid_int, signal.SIGKILL)

    except (FileNotFoundError, ValueError):
        pass

    sys.exit()


@app.command(short_help="Run cloud scan, specify where the scan data is stored (envvar/...)")
def runscan() -> NoReturn:
    print('[bold green] Starting scan ... [/bold green]')

    try:
        scontrol = SensorControler()
    except (CannotReadScanData, RuntimeError, BadManifestSyntax) as e:
        print('[bold red] Error: [/bold red]', e)
        SensorControler.fail_scan(str(e))
        full_exit() # noqa

    print('[bold green] Waiting engine to start ... [/bold green]')
    try:
        scontrol.wait_engine()
    except RuntimeError as e:
        print(f'[bold red] Error waiting for the engine, error: {str(e)} [/bold red]')
        SensorControler.fail_scan(str(e))
        full_exit() # noqa

    # Todo: Retry ?
    is_scan_started, errmsg = scontrol.start_scan()
    if not is_scan_started:
        print(f'[bold red] Error: [/bold red] Scan could not be started. Reason: {errmsg}')
        SensorControler.fail_scan(str(errmsg))
        full_exit() # noqa

    print('[bold green] Scan started')
    print('[bold green] Waiting for scan to finish ... [/bold green]')
    is_scan_finished_with_success = scontrol.wait_scan()
    if not is_scan_finished_with_success:
        print('[bold red] Scan finished with error. [/bold red]')
        SensorControler.fail_scan(str(errmsg))
        full_exit() # noqa

    print('[bold green] Scan finished successfully. [/bold green]')
    print('[bold green] Getting scan results ... [/bold green]')

    # Todo: Retry ?
    gotfindings, scan_report, errmsg = scontrol.get_report()
    if not gotfindings:
        print(f'[bold red] Error: [/bold red] Could not get scan findings. Error: {errmsg}')
        SensorControler.fail_scan(str(errmsg))
        full_exit() # noqa

    # UPLOAD REPORT TO S3 BUCKET
    upload_report_to_s3_bucket(scan_report)

    print('[bold green] Scan findings uploaded to s3 bucket. [/bold green]') # noqa
    SensorControler.finish_scan()
    full_exit()


@app.command(short_help="Stop the current running scan.")
def stopscan() -> NoReturn:
    raise NotImplementedError


@app.command(short_help="Show info about the CLI.")
def info():
    print(f'[bold green] Version: {VERSION}')
    print('Author: Pablo Skubert <pablo1920@protonmail.com>')


def scontroler_main():
    if not DEBUG:
        try:
            app()
        except Exception as middleware_error: # noqa
            print(f'[bold red] Middleware error: {str(middleware_error)} [/bold red]')
            SensorControler.fail_scan(f'Critical middleware error: {str(middleware_error)}')
            full_exit() # noqa
    else:
        # Show full traceback
        app()

