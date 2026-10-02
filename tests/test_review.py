import json
import unittest
from review import review_text


def event(minute, result="failure", source="local"):
    return json.dumps({"time": f"2026-01-01T00:{minute:02d}:00Z", "account": "test", "source": source, "result": result})


class AuthTests(unittest.TestCase):
    def test_burst(self):
        self.assertEqual(review_text("\n".join(event(i) for i in range(5)))[0]["rule"], "failure-burst")

    def test_separated_sources_and_success(self):
        self.assertEqual(review_text("\n".join([event(0), event(1), event(2, source="other"), event(3, "success"), event(10)])), [])

    def test_bad_time_and_event(self):
        for value in ('{"time":"now","account":"a","source":"x","result":"failure"}', "[]", "bad"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                review_text(value)
