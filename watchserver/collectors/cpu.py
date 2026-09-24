from __future__ import annotations

import os

import psutil

from watchserver.models.metrics import CpuFrequency, CpuMetrics


def collect_cpu_metrics() -> CpuMetrics:
    errors: list[str] = []

    try:
        usage_percent = psutil.cpu_percent(interval=0.1)
        per_core_usage_percent = psutil.cpu_percent(interval=None, percpu=True)
    except (OSError, RuntimeError) as exc:
        usage_percent = None
        per_core_usage_percent = []
        errors.append(f"CPU utilization unavailable: {exc}")

    try:
        load_average = os.getloadavg()
    except (AttributeError, OSError) as exc:
        load_average = None
        errors.append(f"load average unavailable: {exc}")

    try:
        raw_frequency = psutil.cpu_freq()
        frequency = (
            CpuFrequency(
                current_mhz=raw_frequency.current,
                min_mhz=raw_frequency.min,
                max_mhz=raw_frequency.max,
            )
            if raw_frequency
            else None
        )
    except (OSError, RuntimeError) as exc:
        frequency = None
        errors.append(f"CPU frequency unavailable: {exc}")

    return CpuMetrics(
        usage_percent=usage_percent,
        per_core_usage_percent=per_core_usage_percent,
        physical_cores=psutil.cpu_count(logical=False),
        logical_cores=psutil.cpu_count(logical=True),
        load_average=load_average,
        frequency=frequency,
        errors=errors,
    )
