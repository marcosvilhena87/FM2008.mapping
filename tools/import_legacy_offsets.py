#!/usr/bin/env python3
"""Converte CSV integral de atribuições IL em JSON de pesquisa NÃO OPERACIONAL."""
import argparse
import csv
import json
from pathlib import Path

REQUIRED = ("type", "loader", "field", "value_decimal", "value_hex", "il_offset")
EDITOR_SHA256 = "e7ba25394eb1f69fc73814a4cbe198a45a5681670f7472a07d9ba9f2a0b3fb07"

def convert(csv_path: Path) -> dict:
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in REQUIRED):
            raise ValueError("Cabeçalho CSV incompatível com offset_assignments.csv")
        entries = []
        keys = set()
        for row_number, row in enumerate(reader, start=2):
            number = int(row["value_decimal"])
            if not -(2**31) <= number < 2**32:
                raise ValueError(f"Linha {row_number}: valor fora de 32 bits")
            if (number & 0xFFFFFFFF) != int(row["value_hex"], 16):
                raise ValueError(f"Linha {row_number}: hex diverge do decimal")
            key = (row["type"], row["loader"], row["field"])
            if key in keys:
                raise ValueError(f"Linha {row_number}: atribuição duplicada {key}")
            keys.add(key)
            entries.append({
                "type": row["type"], "loader": row["loader"],
                "field": row["field"], "valueDecimal": number,
                "ilOffset": row["il_offset"], "status": "legacy-il-observed"
            })
    if not entries:
        raise ValueError("CSV sem atribuições")
    return {
        "kind": "legacy-il-research",
        "editorSha256": EDITOR_SHA256,
        "operational": False,
        "entries": entries
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="offset_assignments.csv original")
    parser.add_argument("--output", type=Path, required=True, help="saída JSON de pesquisa")
    args = parser.parse_args()
    payload = convert(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(payload['entries'])} atribuições importadas como evidência NÃO OPERACIONAL")

if __name__ == "__main__":
    main()
