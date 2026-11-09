"""DNS and TCP reachability diagnostics."""

from network_diagnostics.probe import diagnose, resolve_host, tcp_check

__all__ = ["diagnose", "resolve_host", "tcp_check"]
__version__ = "0.1.0"
