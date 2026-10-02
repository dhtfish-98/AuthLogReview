import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from cli import main


class CLITests(unittest.TestCase):
    def test_finding_json_and_invalid_path(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input"
            payload = '{"time": "2026-01-01T00:00:00Z", "account": "PRIVATE_ACCOUNT", "source": "PRIVATE_SOURCE", "result": "failure"}\n{"time": "2026-01-01T00:01:00Z", "account": "PRIVATE_ACCOUNT", "source": "PRIVATE_SOURCE", "result": "failure"}\n{"time": "2026-01-01T00:02:00Z", "account": "PRIVATE_ACCOUNT", "source": "PRIVATE_SOURCE", "result": "failure"}\n{"time": "2026-01-01T00:03:00Z", "account": "PRIVATE_ACCOUNT", "source": "PRIVATE_SOURCE", "result": "failure"}\n{"time": "2026-01-01T00:04:00Z", "account": "PRIVATE_ACCOUNT", "source": "PRIVATE_SOURCE", "result": "failure"}'
            path.write_bytes(payload if isinstance(payload, bytes) else payload.encode())
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([str(path), "--json"]), 1)
            self.assertTrue(json.loads(output.getvalue()))
            self.assertNotIn("PRIVATE_ACCOUNT", output.getvalue())
            self.assertNotIn("PRIVATE_SOURCE", output.getvalue())
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(path) + ".missing"]), 2)
