#!/usr/bin/env python3
import os, subprocess, sys
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "gxclicker.py")] + sys.argv[1:])
raise SystemExit(0)
