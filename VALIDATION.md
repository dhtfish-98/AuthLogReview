# Validation record

Scope: Five failures for one account/source pair inside five minutes.

Local checks to rerun:

```sh
python -m unittest discover -s tests -v
python cli.py --help
python -m compileall -q review.py cli.py tests
```

Check the exact public GitHub commit and its workflow run separately after publishing. Tests use synthetic input; no production system or external target is exercised. This is an event summary, not an intrusion verdict; log trust, normalization, clock skew and distributed identity correlation remain outside scope.

## Observed local result (2026-10-02)

- Python 3.14.6: 4/4 unit and CLI integration tests passed.
- Analyzer and CLI compiled; CLI help rendered.
- CLI ran with a synthetic finding and JSON output; invalid path returned exit code 2.
- The source and README were reviewed for local-only defensive scope and stated limitations.
- GitHub workflow result must be checked against the exact published commit.
