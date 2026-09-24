from __future__ import annotations

from collections.abc import Iterable


def format_bytes(value: int | None) -> str:
    if value is None:
        return "N/A"

    size = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if size < 1024 or unit == "PB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024

    return "N/A"


def format_percent(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:.1f} %"


def format_duration(seconds: int | None) -> str:
    if seconds is None:
        return "N/A"

    days, remainder = divmod(seconds, 86_400)
    hours, remainder = divmod(remainder, 3_600)
    minutes, _ = divmod(remainder, 60)

    parts: list[str] = []
    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes or not parts:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    return " ".join(parts)


def format_sequence(values: Iterable[float] | None, suffix: str = "") -> str:
    if values is None:
        return "N/A"

    formatted = []
    for value in values:
        formatted.append(f"{value:.2f}{suffix}")
    return " / ".join(formatted) if formatted else "N/A"
