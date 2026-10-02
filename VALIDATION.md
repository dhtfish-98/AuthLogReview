# Validation record

Scope: Five failures for one account/source pair inside five minutes.

Local checks to rerun:

```sh
python -m unittest discover -s tests -v
python cli.py --help
python -m compileall -q review.py cli.py tests
```

Check the exact public GitHub commit and its workflow run separately after publishing. Tests use synthetic input; no production system or external target is exercised. This is an event summary, not an intrusion verdict; log trust, normalization, clock skew and distributed identity correlation remain outside scope.

## Current source result (2026-10-02)

- Python 3.14.6: 8/8 unit and CLI integration tests passed.
- Tests include the specific malformed-input, incomplete-review and declaration cases added during the source audit.
- Malformed/empty identity fields and overflowing timezone conversions are errors. A failure-burst report gives source line numbers, allowing local investigation without emitting account or source identifiers.
- Test input is synthetic. No external target, live credential or production cluster is exercised.
- The public commit and its corresponding GitHub workflow must be verified separately after this update.
