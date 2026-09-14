#!/usr/bin/env bash
cd "$(dirname "$0")"
python3 python/generate_crafts.py
python3 python/web_server.py
