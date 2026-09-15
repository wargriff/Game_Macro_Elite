#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
export PATH="${HOME}/sdk/flutter/bin:${PATH}"

python3 python/generate_crafts.py

echo ""
echo "OrbitWorks Flutter"
echo "=================="
echo "1) App Flutter (recommandé):"
echo "   cd flutter_app && flutter run -d chrome"
echo ""
echo "2) Import pack KSP2 (Windows LocalLow):"
echo "   python3 python/install_to_ksp2.py"
echo ""
echo "Note: KSP2 n'a pas d'import craft 1-clic. Les blueprints servent à"
echo "reconstruire dans le VAB → vrais meshes du jeu."
echo ""

cd flutter_app
flutter pub get
# Prefer chrome if available, else web-server
if flutter devices 2>/dev/null | grep -qi chrome; then
  flutter run -d chrome --web-hostname=127.0.0.1 --web-port=8787
else
  flutter run -d web-server --web-hostname=127.0.0.1 --web-port=8787
fi
