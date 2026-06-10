#!/usr/bin/env python3
"""Obsolète — utilisez OUVRE_MOI.py (seul lanceur quotidien)."""

import warnings

warnings.warn("GO.py est obsolète — utilisez OUVRE_MOI.py", DeprecationWarning, stacklevel=2)

from launcher import main

if __name__ == "__main__":
    raise SystemExit(main())
