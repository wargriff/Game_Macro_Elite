#!/usr/bin/env python3
"""DEPRECIE — utilise START.bat ou gxclicker.py"""
import os, subprocess, sys
root = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(root, "gxclicker.py")] + sys.argv[1:])
raise SystemExit(0)
