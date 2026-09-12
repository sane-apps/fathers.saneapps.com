# `dist/` policy

`dist/` is **generated**. Do not hand-edit it.

Source of truth:

- `scripts/build_site.py`
- `assets/`
- `data/explore/`
- books JSON under `~/SaneApps/clients/translations/books/`

Rebuild:

```bash
~/SaneApps/clients/translations/.venv/bin/python scripts/build_site.py
# or
./scripts/ship.sh --dry-run
```

`dist/` is gitignored. Cloudflare Pages receives the built tree from `scripts/ship.sh`.
