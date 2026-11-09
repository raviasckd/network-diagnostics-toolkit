"""Tests for DNS and TCP probe result handling."""

import socket
import unittest
from unittest.mock import patch

from network_diagnostics.probe import diagnose, resolve_host, tcp_check


class ProbeTests(unittest.TestCase):
    @patch("network_diagnostics.probe.socket.getaddrinfo")
    def test_resolves_and_deduplicates_addresses(self, getaddrinfo) -> None:
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.1", 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.1", 0)),
        ]
        result = resolve_host("example.test")
        self.assertTrue(result["ok"])
        self.assertEqual(result["addresses"], ["192.0.2.1"])

    @patch("network_diagnostics.probe.socket.getaddrinfo", side_effect=socket.gaierror("not found"))
    def test_dns_failure_is_reported(self, _getaddrinfo) -> None:
        result = resolve_host("missing.invalid")
        self.assertFalse(result["ok"])
        self.assertIn("not found", result["error"])

    @patch("network_diagnostics.probe.socket.create_connection")
    def test_tcp_connection_failure_is_reported(self, create_connection) -> None:
        create_connection.side_effect = OSError("connection refused")
        result = tcp_check("example.test", 443, 0.5)
        self.assertFalse(result["ok"])
        self.assertEqual(result["port"], 443)

    @patch("network_diagnostics.probe.resolve_host", return_value={"ok": False, "addresses": [], "error": "DNS error"})
    def test_diagnose_skips_tcp_when_dns_fails(self, resolve) -> None:
        result = diagnose("bad.example", 443)
        self.assertFalse(result["ok"])
        self.assertIsNone(result["tcp"])
        resolve.assert_called_once()


if __name__ == "__main__":
    unittest.main()
