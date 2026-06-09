"""Optional paths for development tools (Node.js, etc.)."""

import os

# Node.js install path on Windows (user: C:\\src)
NODE_PATH = os.environ.get(
    "XCLICKER_NODE_PATH",
    os.environ.get("NODE_HOME", r"C:\src"),
)

# Mission Control dev server (optional — production uses Sidecar port 17840)
MISSION_DEV_PORT = 5173
MISSION_PROD_URL = "http://127.0.0.1:17840/mission"
