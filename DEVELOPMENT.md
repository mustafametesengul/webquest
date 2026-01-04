# Development

Install dependencies:

```bash
uv sync
```

Sort imports:

```bash
uv run ruff check --select I --fix
```

Format code:

```bash
uv run ruff format
```

Generate documentation:

```bash
uv run python scripts/generate_docs.py
```

Run unit tests:

```bash
uv run pytest
```

Run integration tests:

```bash
uv run pytest -m integration
```
