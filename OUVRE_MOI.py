#!/usr/bin/env python3
"""
OUVRE MOI — seul lanceur quotidien.

  Windows  : double-clic OUVRE_MOI.pyw
  PyCharm  : Run OUVRE_MOI.py
  Terminal : python OUVRE_MOI.py

Mission Control ouvre ensuite : native, web, build, .exe.
Réparation : python REPARER.py
"""

from launcher import main

if __name__ == "__main__":
    raise SystemExit(main())
