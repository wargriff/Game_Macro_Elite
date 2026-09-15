# OrbitWorks KSP2 (Flutter)

App **Flutter** pour planifier des crafts KSP2 (Starlink / Starship / fusées / rovers),
avec preview 3D procédurale et pack d’import pour reconstruction VAB.

## Vérité sur les assets & l’import

| Demande | Réalité |
|---------|---------|
| Vrais meshes KSP2 dans l’app | **Non redistribuables** (propriétaires). Preview = reconstruction OrbitWorks. |
| Import 1-clic dans le jeu | **KSP2 n’a pas d’import craft stable** comme KSP1. |
| Jouer avec les vrais modèles | **Oui** : installe le pack → ouvre le blueprint → reconstruis dans le **VAB** (pièces stock). |

## Lancer (Flutter)

```bash
cd OrbitWorks_KSP2
./GO_OrbitWorks.sh
# → Flutter Chrome sur http://127.0.0.1:8787
```

Ou :

```bash
python3 python/generate_crafts.py
cd flutter_app
flutter pub get
flutter run -d chrome --web-hostname=127.0.0.1 --web-port=8787
```

Windows : `GO_OrbitWorks.bat` (Windows desktop ou Chrome).

## Installer le pack dans KSP2

Depuis l’app : bouton **Installer dans KSP2** (desktop), ou :

```bash
python3 python/install_to_ksp2.py
```

Cible typique :

`%USERPROFILE%\AppData\LocalLow\Intercept Games\Kerbal Space Program 2\OrbitWorks_Import\`

Contenu :
- `Blueprints/*.md` — checklist noms affichés stock
- `Vehicles/*.json` — scaffolds expérimentaux
- `LISEZMOI.txt`

## Contenu

67 crafts : Starlink, Starship, fusées planétaires, rovers, comms/data.

## Stack

| Dossier | Rôle |
|---------|------|
| `flutter_app/` | **App principale Flutter** + preview 3D |
| `data/` | Catalogue pièces + recettes |
| `python/` | Générateur blueprints / install pack |
| `export/` | Blueprints + vessels générés |
| `web/` | Ancien viewer Three.js (secondaire) |
