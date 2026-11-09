"""Command-line interface for network diagnostics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from network_diagnostics.probe import diagnose


def _positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("timeout must be greater than zero")
    return number


def _port(value: str) -> int:
    number = int(value)
    if not 1 <= number <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check DNS resolution and optional TCP reachability.")
    parser.add_argument("host", help="Hostname or IP address to check")
    parser.add_argument("--port", type=_port, help="Run one TCP connection check")
    parser.add_argument("--timeout", type=_positive_float, default=3.0)
    parser.add_argument("--json", dest="json_path", type=Path, help="Write report to a JSON file")
    args = parser.parse_args(argv)

    report = diagnose(args.host, args.port, args.timeout)
    print(json.dumps(report, indent=2))
    if args.json_path:
        try:
            args.json_path.write_text(json.dumps(report, indent=2) + "\\n", encoding="utf-8")
        except OSError as exc:
            print(f"network-diagnostics: cannot write report: {exc}", file=sys.stderr)
            return 2
    return 0 if report["ok"] else 1
