#!/usr/bin/env python3
"""Obsolète — utilisez OUVRE_MOI.py."""

import warnings

warnings.warn("main.py est obsolète — utilisez OUVRE_MOI.py", DeprecationWarning, stacklevel=2)

from launcher import main

if __name__ == "__main__":
    raise SystemExit(main())
