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

Run tests:

```bash
uv run pytest
```
