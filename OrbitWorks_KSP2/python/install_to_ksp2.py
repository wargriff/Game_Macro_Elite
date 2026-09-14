#!/usr/bin/env python3
"""Copy OrbitWorks pack next to KSP2 LocalLow folder."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"


def default_dest() -> Path:
    home = Path.home()
    candidates = [
        home / "AppData/LocalLow/Intercept Games/Kerbal Space Program 2",
        home / "AppData/LocalLow/Private Division/Kerbal Space Program 2",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    dest = (args.dest or default_dest()) / "OrbitWorks_Import"
    print("Source:", EXPORT)
    print("Dest  :", dest)
    if args.dry_run:
        return 0
    if not (EXPORT / "Blueprints").exists():
        raise SystemExit("Lance d'abord: python python/generate_crafts.py")
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    shutil.copytree(EXPORT / "Blueprints", dest / "Blueprints")
    pack = EXPORT / "Vehicles" / "KSP2_ImportPack"
    if pack.exists():
        shutil.copytree(pack, dest / "Vehicles")
    else:
        shutil.copytree(EXPORT / "Vehicles", dest / "Vehicles")
    shutil.copy2(EXPORT / "orbitworks_manifest.json", dest / "orbitworks_manifest.json")
    (dest / "LISEZMOI.txt").write_text(
        "OrbitWorks → KSP2\n\n"
        "1) Ouvre les Blueprints/*.md et reconstruis dans le VAB avec les noms affichés.\n"
        "2) Les fichiers Vehicles/*.json sont des scaffolds EXPERIMENTAUX.\n"
        "3) OrbitWorks ne contient PAS les meshes 3D propriétaires du jeu —\n"
        "   utilise les vrais assets en reconstruisant dans le VAB.\n",
        encoding="utf-8",
    )
    print("Installé:", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
