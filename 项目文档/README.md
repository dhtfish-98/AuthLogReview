> 目录已整理：文档在「项目文档」，构建、缓存与暂存输入在「Build」。从仓库根目录运行 `python3 构建.py --build`；如需使用本文原有源码命令，先运行 `python3 构建.py --stage --ci`，再进入 `Build/源码`。暂存会恢复原输入路径。现有版本和历史验证记录按各自提交理解。

# AuthLogReview

Review normalized local authentication event logs for repeated failures. It runs locally, does not contact targets, and reports review prompts instead of exploit instructions.

## Input and checks

- Input: JSONL events from a system you own or are authorized to inspect.
- Checks: Five failures for one account/source pair inside five minutes.
- Output: rule, local location and short note. No source snippets, credential values or log identities are printed.

## Run

```sh
python cli.py ./owned-input
python cli.py ./owned-input --json
python -m unittest discover -s tests -v
```

Exit code 0 means no findings, 1 means review findings, 2 means invalid input or read failure. A clean result is not a security guarantee. The input file is read through a bounded regular-file descriptor with a 4 MiB limit.

## Boundaries

This is an event summary, not an intrusion verdict; log trust, normalization, clock skew and distributed identity correlation remain outside scope. Work only on local, authorized inputs. The analysis does not send data to a service or modify the inspected files.

## Source and policy context

- Technical reference: https://pages.nist.gov/800-63-4/sp800-63b.html
- See [ORIGIN.md](<ORIGIN.md>) for implementation provenance and [VALIDATION.md](<VALIDATION.md>) for checks performed.
- CVP eligibility depends on a real, legitimate defensive task affected by Claude's cyber safeguards and the applicant's organization/identity review; this repository alone does not establish eligibility or approval. [Anthropic CVP guidance](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet).

## Reviewed input behavior

Malformed/empty identity fields and overflowing timezone conversions are errors. A failure-burst report gives source line numbers, allowing local investigation without emitting account or source identifiers.

JSON input rejects duplicate object keys and nonstandard numbers; container nesting is limited to 128 levels.
