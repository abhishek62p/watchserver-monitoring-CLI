from __future__ import annotations

from watchserver.models.metrics import CpuMetrics, DiskMetrics, MemoryMetrics, ServerSnapshot, SystemMetrics
from watchserver.utils.formatting import format_bytes, format_duration, format_percent, format_sequence


WIDTH = 60


def render_server_report(snapshot: ServerSnapshot) -> str:
    sections = [
        _header("WATCH SERVER", "PHASE 1 SERVER METRICS"),
        render_system_report(snapshot.system),
        render_cpu_report(snapshot.cpu),
        render_memory_report(snapshot.memory),
        render_disk_report(snapshot.disk),
        _phase_note(),
        "=" * WIDTH,
    ]
    return "\n\n".join(sections)


def render_system_report(metrics: SystemMetrics) -> str:
    lines = [
        _section("System"),
        _row("Hostname", metrics.hostname),
        _row("OS", f"{metrics.os_name} {metrics.os_version}"),
        _row("Kernel", metrics.kernel),
        _row("Architecture", metrics.architecture),
        _row("Python", metrics.python_version),
        _row("Boot Time", metrics.boot_time.isoformat() if metrics.boot_time else "N/A"),
        _row("Uptime", format_duration(metrics.uptime_seconds)),
    ]
    return _with_errors(lines, metrics.errors)


def render_cpu_report(metrics: CpuMetrics) -> str:
    frequency = "N/A"
    if metrics.frequency is not None:
        frequency = f"{metrics.frequency.current_mhz:.0f} MHz"

    lines = [
        _section("CPU"),
        _row("Usage", format_percent(metrics.usage_percent)),
        _row("Physical Cores", metrics.physical_cores if metrics.physical_cores is not None else "N/A"),
        _row("Logical Cores", metrics.logical_cores if metrics.logical_cores is not None else "N/A"),
        _row("Load Average", format_sequence(metrics.load_average)),
        _row("CPU Frequency", frequency),
        _row("Per-Core Usage", format_sequence(metrics.per_core_usage_percent, suffix="%")),
    ]
    return _with_errors(lines, metrics.errors)


def render_memory_report(metrics: MemoryMetrics) -> str:
    lines = [
        _section("Memory"),
        _row("Total", format_bytes(metrics.total_bytes)),
        _row("Used", format_bytes(metrics.used_bytes)),
        _row("Available", format_bytes(metrics.available_bytes)),
        _row("Usage", format_percent(metrics.percent_used)),
        _row("Swap Total", format_bytes(metrics.swap_total_bytes)),
        _row("Swap Used", format_bytes(metrics.swap_used_bytes)),
        _row("Swap Usage", format_percent(metrics.swap_percent_used)),
    ]
    return _with_errors(lines, metrics.errors)


def render_disk_report(metrics: DiskMetrics) -> str:
    lines = [_section("Disk")]
    for filesystem in metrics.filesystems:
        lines.append(_row("Filesystem", filesystem.path))
        if filesystem.error:
            lines.append(_row("Status", filesystem.error))
        else:
            lines.extend(
                [
                    _row("Total", format_bytes(filesystem.total_bytes)),
                    _row("Used", format_bytes(filesystem.used_bytes)),
                    _row("Free", format_bytes(filesystem.free_bytes)),
                    _row("Usage", format_percent(filesystem.percent_used)),
                ]
            )
        lines.append("-" * WIDTH)
    if lines[-1] == "-" * WIDTH:
        lines.pop()
    return "\n".join(lines)


def _header(title: str, subtitle: str) -> str:
    return "\n".join(
        [
            "=" * WIDTH,
            title.center(WIDTH),
            subtitle.center(WIDTH),
            "=" * WIDTH,
        ]
    )


def _section(title: str) -> str:
    return "\n".join([title, "-" * WIDTH])


def _row(label: str, value: object) -> str:
    return f"{label:<16}: {value}"


def _with_errors(lines: list[str], errors: list[str]) -> str:
    for error in errors:
        lines.append(_row("Warning", error))
    return "\n".join(lines)


def _phase_note() -> str:
    return "\n".join(
        [
            "Phase Status",
            "-" * WIDTH,
            _row("Implemented", "System, CPU, memory, disk collection"),
            _row("Health Status", "Planned for Phase 3"),
            _row("Config File", "Planned for Phase 4"),
        ]
    )
