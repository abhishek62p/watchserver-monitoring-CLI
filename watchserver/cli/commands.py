from __future__ import annotations

import argparse
from collections.abc import Sequence

from watchserver.app import DEFAULT_DISK_PATHS, collect_phase1_snapshot
from watchserver.collectors.cpu import collect_cpu_metrics
from watchserver.collectors.disk import collect_disk_metrics
from watchserver.collectors.memory import collect_memory_metrics
from watchserver.collectors.system import collect_system_metrics
from watchserver.models.metrics import ServerSnapshot
from watchserver.reporters.terminal import (
    render_cpu_report,
    render_disk_report,
    render_memory_report,
    render_server_report,
    render_system_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="watchserver",
        description="Watch Server Phase 1: collect Linux system, CPU, memory, and disk metrics.",
    )
    parser.add_argument(
        "--disk-path",
        action="append",
        dest="disk_paths",
        help="Filesystem path to inspect. Repeat to inspect multiple paths. Defaults to /.",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("system", help="Display system information.")
    subparsers.add_parser("cpu", help="Display CPU metrics.")
    subparsers.add_parser("memory", help="Display memory metrics.")
    subparsers.add_parser("disk", help="Display disk metrics.")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    disk_paths = args.disk_paths or list(DEFAULT_DISK_PATHS)

    if args.command == "system":
        print(render_system_report(collect_system_metrics()))
        return 0
    if args.command == "cpu":
        print(render_cpu_report(collect_cpu_metrics()))
        return 0
    if args.command == "memory":
        print(render_memory_report(collect_memory_metrics()))
        return 0
    if args.command == "disk":
        print(render_disk_report(collect_disk_metrics(disk_paths)))
        return 0

    snapshot = collect_phase1_snapshot(disk_paths)
    print(render_server_report(snapshot))
    return _exit_code_for_snapshot(snapshot)


def _exit_code_for_snapshot(snapshot: ServerSnapshot) -> int:
    """Return non-zero only when every requested disk failed.

    Phase 1 does not evaluate health yet, but it should still communicate a
    completely unusable disk request to shell automation.
    """

    if snapshot.disk.filesystems and all(item.error for item in snapshot.disk.filesystems):
        return 2
    return 0
