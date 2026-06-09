"""Compat PyCharm — delegue a launch.run (sans import ui.*)."""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.bootstrap import ensure_project_ready

ensure_project_ready(ROOT)

from launch import run

if __name__ == "__main__":
    raise SystemExit(run())
