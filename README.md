# Network Diagnostics Toolkit

A lightweight, dependency-free Python CLI for checking DNS resolution and TCP reachability of a host.

## What it checks

- Resolves a hostname using the system resolver.
- Optionally attempts a TCP connection to a specified port.
- Applies an explicit timeout to network operations.
- Emits a readable summary or machine-readable JSON.
- Reports failures without hiding the underlying socket error.

The tool performs only the checks requested by the operator. It does not scan port ranges or attempt authentication.

## Requirements

- Python 3.10+
- No third-party runtime dependencies

## Usage

```bash
python -m network_diagnostics example.com
python -m network_diagnostics example.com --port 443 --timeout 3
python -m network_diagnostics example.com --port 443 --json report.json
```

Install as a local package:

```bash
python -m pip install .
network-diagnostics example.com --port 443
```

## Development

```bash
python -m unittest discover -s tests -v
```

## Scope

This is an operator-invoked connectivity check, not a vulnerability scanner or an uptime monitoring service. Results depend on the local resolver, routing, firewall policy, and target availability.

## License

MIT. See [LICENSE](LICENSE).
