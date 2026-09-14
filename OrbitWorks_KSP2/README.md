# OrbitWorks KSP2

Plans de **fusées / Starlink / Starship / rovers** pour **Kerbal Space Program 2**, avec IDs de pièces stock, blueprints VAB, et viewer 3D procédural.

## Assets 3D du jeu (important)

Les meshes et textures officiels KSP2 sont **propriétaires**. OrbitWorks **ne les extrait pas et ne les redistribue pas**.

- La vue 3D = **reconstruction procédurale** (silhouette Starship, bus Starlink, fusées, rovers).
- Pour jouer avec les **vrais modèles du jeu** : reconstruis chaque craft dans le **VAB** en suivant le blueprint (noms affichés stock).

## Lancer

```bash
cd OrbitWorks_KSP2
python3 python/generate_crafts.py
python3 python/web_server.py
```

→ http://127.0.0.1:8777/

Windows : `GO_OrbitWorks.bat`

## Contenu généré

- Starlink (rideshare, SSO, polar, GTO, MEO, HEO, DTC, déploiement Starship…)
- Starship-K (crew, cargo, tanker, Mun/Duna, hop, depot…)
- Fusées planétaires
- Rovers
- Comms / Data

## Import dans le vrai jeu

```bash
python3 python/install_to_ksp2.py
```

Cible typique Windows :

`%USERPROFILE%\AppData\LocalLow\Intercept Games\Kerbal Space Program 2\OrbitWorks_Import\`

1. Ouvre le `.md` blueprint du craft
2. Dans le VAB, cherche chaque **nom affiché**
3. Assemble selon l’ordre suggéré
4. Sauvegarde le véhicule dans KSP2

Les `Vehicles/*.json` sont des **scaffolds expérimentaux**, pas un format craft officiel.

## Stack

| Dossier | Rôle |
|---------|------|
| `data/` | Catalogue pièces + recettes |
| `python/` | Générateur, serveur, install |
| `web/` | UI 3D Three.js |
| `export/` | Blueprints + vessels |

## Modifier un modèle

Édite `data/craft_recipes.json` puis relance `python3 python/generate_crafts.py`.
