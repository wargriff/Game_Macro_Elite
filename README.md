# GAMEX_MACRO (Game_Macro_elite)

Suite gaming **GAMEX CLICKER** — concurrent iCUE / G HUB / Synapse (Qt6 Widgets + QSS + assets SVG premium).

## Prerequis

1. **Qt 6.5+** avec modules **Widgets** et **Svg**
   - https://www.qt.io/download
   - Ou : `winget install Qt.Qt.6.8.0.Microsoft.Windows.SDK`

2. **CMake 3.16+** et **MSVC 2022**

## Build

```powershell
$env:CMAKE_PREFIX_PATH = "C:\Qt\6.8.0\msvc2022_64"
cmake -S C:\Users\wargriff\visual_studio_project\Game_Macro_elite -B C:\Users\wargriff\visual_studio_project\Game_Macro_elite\build
cmake --build C:\Users\wargriff\visual_studio_project\Game_Macro_elite\build --config Release
```

Executable : `build\Release\GAMEX_MACRO.exe`

## Resources & AssetGenerator

Arborescence `resources/` :

```
resources/
├── icons/          # Navigation sidebar (SVG)
├── devices/        # Clavier, souris, GPU, dock tiles…
├── previews/       # Aperçus RGB (+ PNG 4K générés)
├── wallpapers/     # Fonds cyberpunk GAMEX
├── logos/          # Logo et marque G
├── avatars/        # Profils jeux (Diablo IV…)
├── themes/         # gamex-dark.json
└── animations/     # glow-pulse.svg
```

Au démarrage, `AssetGenerator` :
- crée les dossiers manquants ;
- génère tout SVG absent depuis des templates premium ;
- rend les PNG 4K (3840×2160) depuis les SVG pour previews/wallpapers.

Aucune image temporaire — assets vectoriels + rendu Qt6.

## UI

**Device Center** : clavier 60% RGB, panneau TOUCHE W, effets lumineux, stats macros, dock 8 périphériques — aligné sur la maquette rouge GAMEX.

## Projet lie

- `Game_macro_Clicker` (SFML) — version SFML dans le dossier voisin.
