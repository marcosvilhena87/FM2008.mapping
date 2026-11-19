#!/usr/bin/env python3
"""Offline comparison of legacy-probe observations with independently reviewed references.

Never opens fm.exe, never modifies saves or memory, never approves a map.
A copied probe output is NOT an independent source.
"""
import argparse
import csv
import json
import unicodedata
from collections import Counter
from pathlib import Path

OBSERVED_COLUMNS = ("save_id", "index", "id", "first_name", "last_name", "common_name")
REFERENCE_COLUMNS = (
    "save_id", "observed_index", "reference_id", "first_name",
    "last_name", "common_name", "source_type", "source_detail", "reviewer"
)
INDEPENDENT_ID_SOURCES = {"independent_database", "independent_tool"}
ACCEPTED_SOURCES = INDEPENDENT_ID_SOURCES | {"game_ui"}
DISALLOWED_ORIGINS = {"readonlyprobe", "fmrte2008", "same_probe", "probe_output"}


def read_csv(path, fields):
    with open(path, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or any(field not in reader.fieldnames for field in fields):
            raise ValueError(f"{path}: colunas necessárias: {', '.join(fields)}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path}: sem registros")
    return rows


def normalized(value):
    return "".join(
        c for c in unicodedata.normalize("NFKD", (value or "").strip()).casefold()
        if not unicodedata.combining(c)
    )


def verify(observed_rows, reference_rows):
    observed = {}
    for row in observed_rows:
        key = (row["save_id"], row["index"])
        if key in observed:
            raise ValueError(f"Observação duplicada: {key}")
        if not row["id"].isdigit() or int(row["id"]) <= 0 or not row["index"].isdigit():
            raise ValueError(f"ID ou índice inválido: {key}")
        observed[key] = row

    entries = []
    used = set()
    for row in reference_rows:
        key = (row["save_id"], row["observed_index"])
        if key in used:
            raise ValueError(f"Referência duplicada: {key}")
        used.add(key)
        if key not in observed:
            raise ValueError(f"Referência sem observação correspondente: {key}")
        o = observed[key]
        source = row["source_type"].strip().casefold()
        detail = row["source_detail"].strip()
        reviewer = row["reviewer"].strip()
        ref_id = row["reference_id"].strip()

        # A filled-in template is not a confirmed observation. Explicit
        # human provenance is required even to claim an independently seen name.
        reviewed = (source in ACCEPTED_SOURCES and bool(reviewer) and
                    bool(detail) and not normalized(detail).startswith("confirmar no perfil") and
                    all(bad not in normalized(detail) for bad in DISALLOWED_ORIGINS))
        status = "pending"
        if reviewed:
            names_match = (
                normalized(o["first_name"]) == normalized(row["first_name"]) and
                normalized(o["last_name"]) == normalized(row["last_name"]) and
                normalized(o["common_name"]) == normalized(row["common_name"])
            )
            if not names_match:
                status = "mismatch"
            elif ref_id:
                if not ref_id.isdigit() or int(ref_id) <= 0:
                    status = "invalid_reference_id"
                elif source not in INDEPENDENT_ID_SOURCES:
                    # The game's UI usually shows names but not internal IDs.
                    status = "name_only"
                elif int(ref_id) != int(o["id"]):
                    status = "mismatch"
                else:
                    status = "id_and_name_match"
            else:
                status = "name_only"
        entries.append({
            "save_id": key[0], "index": int(key[1]), "observed_id": int(o["id"]),
            "reference_id": int(ref_id) if ref_id.isdigit() else None,
            "source_type": source, "reviewer": reviewer if reviewed else None,
            "status": status,
        })

    counts = Counter(row["status"] for row in entries)
    return {
        "schema_version": 1,
        "operational": False, "approved": False,
        "observed_count": len(observed),
        "compared_count": len(entries),
        "status_counts": dict(sorted(counts.items())),
        "independently_confirmed_ids": counts["id_and_name_match"],
        "all_ids_independently_confirmed": (
            bool(entries) and len(entries) == len(observed)
            and counts["id_and_name_match"] == len(observed)
        ),
        "note": "Relatório documental: não aprova mapa nem verifica autenticidade externa da referência.",
        "entries": entries,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observed", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = verify(read_csv(args.observed, OBSERVED_COLUMNS),
                    read_csv(args.reference, REFERENCE_COLUMNS))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Confrontados: {report['compared_count']} / {report['observed_count']}")
    print("Resultado:", report["status_counts"])
    print("IDs com documentação independente:", report["independently_confirmed_ids"])
    print("Mapa operacional aprovado: NÃO")


if __name__ == "__main__":
    main()
