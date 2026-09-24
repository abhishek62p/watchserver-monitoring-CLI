from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True)
class SystemMetrics:
    hostname: str
    os_name: str
    os_version: str
    kernel: str
    architecture: str
    python_version: str
    boot_time: datetime | None
    uptime_seconds: int | None
    errors: list[str]


@dataclass(frozen=True)
class CpuFrequency:
    current_mhz: float
    min_mhz: float
    max_mhz: float


@dataclass(frozen=True)
class CpuMetrics:
    usage_percent: float | None
    per_core_usage_percent: list[float]
    physical_cores: int | None
    logical_cores: int | None
    load_average: tuple[float, float, float] | None
    frequency: CpuFrequency | None
    errors: list[str]


@dataclass(frozen=True)
class MemoryMetrics:
    total_bytes: int | None
    available_bytes: int | None
    used_bytes: int | None
    percent_used: float | None
    swap_total_bytes: int | None
    swap_used_bytes: int | None
    swap_percent_used: float | None
    errors: list[str]


@dataclass(frozen=True)
class DiskUsage:
    path: str
    total_bytes: int | None
    used_bytes: int | None
    free_bytes: int | None
    percent_used: float | None
    error: str | None


@dataclass(frozen=True)
class DiskMetrics:
    filesystems: list[DiskUsage]


@dataclass(frozen=True)
class ServerSnapshot:
    timestamp: datetime
    system: SystemMetrics
    cpu: CpuMetrics
    memory: MemoryMetrics
    disk: DiskMetrics

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        if self.system.boot_time is not None:
            data["system"]["boot_time"] = self.system.boot_time.isoformat()
        return data
