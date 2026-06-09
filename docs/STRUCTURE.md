# Structure du projet v3.0

```
Game_XClicker_Elite/
├── START.bat              # Lanceur Windows (double-clic)
├── REPARER.bat            # Sync GitHub + deps + lancement
├── CLONE_FRESH.bat        # Installation propre depuis zero
├── main.py                # Point d'entree PyCharm
├── gxclicker.py           # Application (moteur + fenetre web)
├── build.spec             # PyInstaller → .exe
├── ui-web/                # Interface iCUE (HTML/CSS/JS)
│   ├── index.html
│   ├── css/
│   └── js/
├── assets/
│   └── brand/             # Icone SOURIS WARGRIFF, favicon
├── core/                  # Moteur Win32 macros
├── services/              # API Sidecar :17840, Node bridge :5173
├── nodejs/                # Proxy UI (optionnel)
├── profiles/              # Profils JSON
├── config/                # Chemins assets, runtime
├── scripts/               # generate_icon.py, etc.
└── pycharm/               # Config Run PyCharm a importer
```

## Lancement

| Action | Commande |
|--------|----------|
| Usage quotidien | Double-clic `START.bat` |
| Premiere install / reparation | `REPARER.bat` |
| Clone propre | `CLONE_FRESH.bat` |
| PyCharm | Script `main.py` |
| Navigateur seul | `START.bat browser` |
| Build .exe | `START.bat build` |

## Architecture

```
START.bat → main.py → gxclicker.py
                          ├─ core/ MacroManager (Win32)
                          ├─ services/sidecar_api.py  → http://127.0.0.1:17840
                          ├─ services/node_bridge.py  → http://127.0.0.1:5173 (optionnel)
                          └─ pywebview ou navigateur
```

## 6 macros (sidebar)

| Sidebar | Touche |
|---------|--------|
| MACRO 1 | left |
| MACRO 2 | right |
| MACRO 3 | 1 |
| MACRO 4 | 2 |
| MACRO 5 | 3 |
| MACRO 6 | 4 |

## PyQt legacy (optionnel)

`Xmacro_main.py` + dossier `ui/` = ancienne interface PyQt6. Non utilise par `START.bat`.
