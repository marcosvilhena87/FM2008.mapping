#!/usr/bin/env python3
"""Validação estrutural offline de manifestos. Requer pip install jsonschema."""
import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit("Instale a dependência: python -m pip install jsonschema") from exc

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / "schemas/mapping.schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema)
files = sorted((ROOT / "maps").rglob("*.json"))
if not files:
    raise SystemExit("Nenhum mapa encontrado")
for path in files:
    item = json.loads(path.read_text(encoding="utf-8"))
    errors = sorted(validator.iter_errors(item), key=lambda error: list(map(str, error.path)))
    if errors:
        for err in errors:
            print(f"{path.relative_to(ROOT)}: {list(err.path)}: {err.message}")
        raise SystemExit(1)
    print(f"OK: {path.relative_to(ROOT)}")
print(f"{len(files)} manifesto(s) válido(s)")
