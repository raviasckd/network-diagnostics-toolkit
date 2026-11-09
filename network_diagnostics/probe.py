"""Small, bounded DNS and TCP connectivity probes."""

from __future__ import annotations

import socket
from time import perf_counter
from typing import Any


def resolve_host(host: str) -> dict[str, Any]:
    """Resolve a host and return unique IP addresses or a resolver error."""
    try:
        records = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except (OSError, socket.gaierror) as exc:
        return {"ok": False, "addresses": [], "error": str(exc)}

    addresses = sorted({record[4][0] for record in records})
    return {"ok": bool(addresses), "addresses": addresses, "error": None}


def tcp_check(host: str, port: int, timeout: float = 3.0) -> dict[str, Any]:
    """Attempt one TCP connection; never retries or scans additional ports."""
    started = perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed_ms = round((perf_counter() - started) * 1000, 2)
        return {"ok": True, "port": port, "duration_ms": elapsed_ms, "error": None}
    except OSError as exc:
        elapsed_ms = round((perf_counter() - started) * 1000, 2)
        return {"ok": False, "port": port, "duration_ms": elapsed_ms, "error": str(exc)}


def diagnose(host: str, port: int | None = None, timeout: float = 3.0) -> dict[str, Any]:
    """Run DNS resolution and, when requested, a single TCP connectivity test."""
    dns_result = resolve_host(host)
    tcp_result = tcp_check(host, port, timeout) if port is not None and dns_result["ok"] else None
    ok = dns_result["ok"] and (tcp_result is None or tcp_result["ok"])
    return {"host": host, "dns": dns_result, "tcp": tcp_result, "ok": ok}
