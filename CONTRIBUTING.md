# Contributing

## Development setup

Requires Python 3.12+.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest -q
.venv/bin/uvicorn app.main:app --reload
```

`make` targets wrap the same commands (`make install`, `make test`,
`make docker-build`) but a local `make` is not required; run the underlying
commands directly.

## Conventions

- `ruff check` and `ruff format` must pass; `bandit` and `mypy` must be clean.
- Keep runtime dependencies minimal and pinned in `requirements.txt`.
- Commits: imperative mood, concise subject line.
- Update `CHANGELOG.md` under `Unreleased` for user-visible changes.

## Pull requests

- CI must be green: lint, format, tests, coverage >= 80%, Trivy image scan.
- Keep PRs focused; link related issues.
