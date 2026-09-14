#!/usr/bin/env python3
"""Génère blueprints VAB + scaffolds vessel JSON pour KSP2 (pièces stock)."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EXPORT = ROOT / "export"
BLUEPRINTS = EXPORT / "Blueprints"
VEHICLES = EXPORT / "Vehicles"
IMPORT_PACK = VEHICLES / "KSP2_ImportPack"
WEB = ROOT / "web"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def part_lookup(catalog: dict) -> dict:
    return {p["id"]: p for p in catalog["parts"]}


def dest_lookup(recipes_doc: dict) -> dict:
    return {d["id"]: d for d in recipes_doc.get("destinations", [])}


def category_of(recipe: dict) -> str:
    subtype = recipe.get("subtype") or ""
    preview = recipe.get("preview") or ""
    typ = recipe.get("type") or ""
    if subtype == "starlink" or preview == "starlink":
        return "starlink"
    if subtype == "starship" or preview == "starship":
        return "starship"
    if subtype == "comms":
        return "comms"
    if subtype == "data":
        return "data"
    if typ == "rover":
        return "rovers"
    if typ == "rocket":
        return "rockets"
    return typ or "misc"


def stack_items(recipe: dict) -> list[dict]:
    if "stack" in recipe:
        return [{"id": s["part"], "qty": int(s.get("qty", 1)), "role": s.get("role", "")} for s in recipe["stack"]]
    if "parts" in recipe:
        return [{"id": p["id"], "qty": int(p.get("qty", 1)), "role": p.get("role", "")} for p in recipe["parts"]]
    raise KeyError(f"Pas de stack/parts dans {recipe.get('id')}")


def resolve_parts(recipe: dict, parts: dict) -> list[dict]:
    resolved = []
    for item in stack_items(recipe):
        pid = item["id"]
        qty = item["qty"]
        if pid not in parts:
            raise KeyError(f"Pièce inconnue dans {recipe['id']}: {pid}")
        meta = parts[pid]
        display = meta.get("display_name") or meta.get("name") or pid
        unit = float(meta.get("mass_t", 0))
        resolved.append(
            {
                "part_id": pid,
                "display_name": display,
                "category": meta.get("category", ""),
                "role": item.get("role", ""),
                "qty": qty,
                "mass_t": unit * qty,
                "unit_mass_t": unit,
            }
        )
    return resolved


def estimate_dv(recipe: dict, destinations: dict, total_mass: float) -> int:
    dest = destinations.get(recipe.get("destination") or "", {})
    if dest.get("dv"):
        return int(dest["dv"])
    base = {
        "starlink": 3400,
        "starship": 9000,
        "rockets": 6200,
        "rovers": 450,
        "comms": 3000,
        "data": 2800,
    }.get(category_of(recipe), 3200)
    return base + int(min(2000, total_mass * 25))


def write_blueprint(recipe: dict, resolved: list[dict], total_mass: float, dv: int, dest_name: str) -> Path:
    BLUEPRINTS.mkdir(parents=True, exist_ok=True)
    cat = category_of(recipe)
    lines = [
        f"# {recipe['name']}",
        "",
        f"**OrbitWorks ID:** `{recipe['id']}`",
        f"**Catégorie:** {cat}",
        f"**Type / sous-type:** {recipe.get('type')} / {recipe.get('subtype')}",
        f"**Destination:** {dest_name}",
        f"**Masse estimée:** {total_mass:.3f} t",
        f"**Δv estimé (indicatif):** ~{dv} m/s",
        "",
        "## Important — KSP 2",
        "",
        "KSP2 n'a pas d'import craft 1-clic stable comme KSP1.",
        "Reconstruisez ce vaisseau dans le **VAB** avec les pièces stock ci-dessous",
        "(noms affichés = ceux du jeu). Les meshes/textures restent ceux de votre installation.",
        "",
        "## Checklist pièces (stock KSP2)",
        "",
        "| Qty | Nom affiché (jeu) | ID interne | Rôle | Masse ligne (t) |",
        "|----:|-------------------|------------|------|----------------:|",
    ]
    for p in resolved:
        lines.append(
            f"| {p['qty']} | {p['display_name']} | `{p['part_id']}` | {p['role'] or '—'} | {p['mass_t']:.3f} |"
        )
    lines += [
        "",
        "## Ordre de montage suggéré (bas → haut)",
        "",
        "1. Moteurs / boosters + réservoirs bas",
        "2. Découpleurs / séparateurs",
        "3. Étage supérieur + avionique",
        "4. Payload (sats / cargo / rover)",
        "5. Coiffe / aéro / ailerons Starship",
        "",
        "## Notes",
        "",
        recipe.get("notes") or "—",
        "",
        f"_Généré {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} — OrbitWorks_",
        "",
    ]
    path = BLUEPRINTS / f"{recipe['id']}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_vessel_scaffold(recipe: dict, resolved: list[dict], total_mass: float, cat: str) -> tuple[Path, Path]:
    VEHICLES.mkdir(parents=True, exist_ok=True)
    IMPORT_PACK.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "orbitworks.ksp2.vessel_scaffold/1",
        "warning": (
            "Scaffold expérimental — pas un fichier craft KSP2 officiel. "
            "Utilisez le blueprint Markdown pour reconstruire dans le VAB."
        ),
        "metadata": {
            "id": recipe["id"],
            "name": recipe["name"],
            "category": cat,
            "type": recipe.get("type"),
            "subtype": recipe.get("subtype"),
            "destination": recipe.get("destination"),
            "tags": recipe.get("tags", []),
            "preview": recipe.get("preview"),
            "total_mass_t": round(total_mass, 4),
        },
        "assembly": [
            {
                "partName": p["part_id"],
                "displayName": p["display_name"],
                "quantity": p["qty"],
                "role": p["role"],
                "mass_t": p["unit_mass_t"],
            }
            for p in resolved
        ],
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    vessel = VEHICLES / f"{recipe['id']}.vessel.json"
    vessel.write_text(text, encoding="utf-8")
    pack = IMPORT_PACK / f"{recipe['id']}.json"
    pack.write_text(text, encoding="utf-8")
    return vessel, pack


def main() -> None:
    catalog = load_json(DATA / "parts_catalog.json")
    recipes_doc = load_json(DATA / "craft_recipes.json")
    recipes = recipes_doc["crafts"]
    parts = part_lookup(catalog)
    destinations = dest_lookup(recipes_doc)

    if EXPORT.exists():
        shutil.rmtree(EXPORT)
    BLUEPRINTS.mkdir(parents=True)
    VEHICLES.mkdir(parents=True)
    IMPORT_PACK.mkdir(parents=True)

    crafts_out = []
    for recipe in recipes:
        resolved = resolve_parts(recipe, parts)
        total_mass = sum(p["mass_t"] for p in resolved)
        cat = category_of(recipe)
        dest_id = recipe.get("destination") or ""
        dest_meta = destinations.get(dest_id, {})
        dest_name = dest_meta.get("name") or dest_id or "N/A"
        dv = estimate_dv(recipe, destinations, total_mass)
        bp = write_blueprint(recipe, resolved, total_mass, dv, dest_name)
        vessel, _pack = write_vessel_scaffold(recipe, resolved, total_mass, cat)
        crafts_out.append(
            {
                "id": recipe["id"],
                "name": recipe["name"],
                "category": cat,
                "type": recipe.get("type"),
                "subtype": recipe.get("subtype"),
                "preview": recipe.get("preview") or cat,
                "destination": dest_name,
                "destination_id": dest_id,
                "tags": recipe.get("tags", []),
                "notes": recipe.get("notes", ""),
                "parts_count": sum(p["qty"] for p in resolved),
                "mass_t": round(total_mass, 4),
                "estimated_dv_ms": dv,
                "blueprint_file": str(bp.relative_to(EXPORT)).replace("\\", "/"),
                "vessel_file": str(vessel.relative_to(EXPORT)).replace("\\", "/"),
                "parts": resolved,
            }
        )

    by_cat: dict[str, int] = {}
    for c in crafts_out:
        by_cat[c["category"]] = by_cat.get(c["category"], 0) + 1

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tool": "OrbitWorks KSP2",
        "ksp2_note": (
            "Blueprints = checklist VAB avec noms de pièces stock. "
            "Les modèles 3D du jeu restent dans votre installation KSP2 (non redistribués). "
            "La vue OrbitWorks est une reconstruction procédurale fidèle à la silhouette."
        ),
        "parts_catalog_version": catalog.get("version") or catalog.get("meta", {}).get("game"),
        "count": len(crafts_out),
        "by_category": by_cat,
        "crafts": crafts_out,
    }
    (EXPORT / "orbitworks_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    WEB.mkdir(parents=True, exist_ok=True)
    (WEB / "catalog.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"OK — {len(crafts_out)} crafts générés")
    for k, v in sorted(by_cat.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
