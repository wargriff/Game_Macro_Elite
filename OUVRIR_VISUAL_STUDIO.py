#!/usr/bin/env python3
"""
Ouvre Game_XClicker_Elite.sln dans Visual Studio.
Contourne le blocage Smart App Control des fichiers .bat.

  python OUVRIR_VISUAL_STUDIO.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
INCLUDE = os.path.join(ROOT, "cpp", "third_party", "include")


def unblock_tree() -> None:
    if sys.platform != "win32":
        return
    ps = (
        f"Get-ChildItem -LiteralPath '{ROOT}' -Recurse -Force "
        f"| Unblock-File -ErrorAction SilentlyContinue"
    )
    subprocess.call(
        ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps],
        cwd=ROOT,
    )


def fetch_deps() -> None:
    os.makedirs(INCLUDE, exist_ok=True)
    os.makedirs(os.path.join(INCLUDE, "nlohmann"), exist_ok=True)
    files = {
        "httplib.h": "https://raw.githubusercontent.com/yhirose/cpp-httplib/v0.15.3/httplib.h",
        "nlohmann/json.hpp": (
            "https://raw.githubusercontent.com/nlohmann/json/v3.11.3/"
            "single_include/nlohmann/json.hpp"
        ),
    }
    for rel, url in files.items():
        dest = os.path.join(INCLUDE, rel.replace("/", os.sep))
        if os.path.isfile(dest):
            print(f"  OK {rel}")
            continue
        print(f"  -> {rel}")
        urllib.request.urlretrieve(url, dest)


def open_visual_studio() -> int:
    sln = os.path.join(ROOT, "Game_XClicker_Elite.sln")
    if not os.path.isfile(sln):
        print("ERREUR: Game_XClicker_Elite.sln introuvable")
        print("Lancez: git pull origin main")
        input("Entree...")
        return 1

    if sys.platform == "win32":
        os.startfile(sln)  # type: ignore[attr-defined]
    else:
        subprocess.Popen(["xdg-open", sln])
    return 0


def main() -> int:
    os.chdir(ROOT)
    print("=" * 50)
    print("  OUVRIR VISUAL STUDIO — Game XClicker Elite")
    print("=" * 50)
    print("\n[1/3] Debloquage fichiers...")
    unblock_tree()
    print("\n[2/3] Dependances C++ (httplib, json)...")
    fetch_deps()
    print("\n[3/3] Ouverture Game_XClicker_Elite.sln ...")
    print("\nDans VS: Release | x64 > Generer > F5")
    print("Projet demarrage: GameXClicker\n")
    return open_visual_studio()


if __name__ == "__main__":
    raise SystemExit(main())
