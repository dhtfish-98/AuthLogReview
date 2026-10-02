import json
import plistlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from review import review_text


class RegressionTests(unittest.TestCase):

    def test_overflow_and_empty_identity(self):
        event={"time":"0001-01-01T00:00:00+23:59","account":"synthetic","source":"local","result":"failure"}
        with self.assertRaises(ValueError): review_text(json.dumps(event))
        event.update(time="2026-01-01T00:00:00Z",account="")
        with self.assertRaises(ValueError): review_text(json.dumps(event))
    def test_actionable_lines_without_identities(self):
        events=[json.dumps({"time":f"2026-01-01T00:0{i}:00Z","account":"PRIVATE_ACCOUNT","source":"PRIVATE_SOURCE","result":"failure"}) for i in (4,0,3,1,2)]
        findings=review_text("\n".join(events))
        self.assertEqual(findings[0]["location"],"lines 1,2,3,4,5")
        self.assertNotIn("PRIVATE_ACCOUNT",repr(findings))
