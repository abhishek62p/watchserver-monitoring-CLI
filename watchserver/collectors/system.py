from __future__ import annotations

import platform
import socket
import sys
from datetime import datetime, timezone

import psutil

from watchserver.models.metrics import SystemMetrics


def collect_system_metrics() -> SystemMetrics:
    errors: list[str] = []

    try:
        hostname = socket.gethostname()
    except OSError as exc:
        hostname = "N/A"
        errors.append(f"hostname unavailable: {exc}")

    try:
        system = platform.uname()
        os_name = system.system or "N/A"
        os_version = system.release or "N/A"
        kernel = system.version or "N/A"
        architecture = system.machine or "N/A"
    except (OSError, RuntimeError) as exc:
        os_name = os_version = kernel = architecture = "N/A"
        errors.append(f"system information unavailable: {exc}")

    python_version = platform.python_version() or sys.version.split()[0]

    try:
        boot_timestamp = psutil.boot_time()
        boot_time = datetime.fromtimestamp(boot_timestamp, tz=timezone.utc)
        uptime_seconds = max(0, int(datetime.now(timezone.utc).timestamp() - boot_timestamp))
    except (OSError, RuntimeError, ValueError) as exc:
        boot_time = None
        uptime_seconds = None
        errors.append(f"boot time unavailable: {exc}")

    return SystemMetrics(
        hostname=hostname,
        os_name=os_name,
        os_version=os_version,
        kernel=kernel,
        architecture=architecture,
        python_version=python_version,
        boot_time=boot_time,
        uptime_seconds=uptime_seconds,
        errors=errors,
    )