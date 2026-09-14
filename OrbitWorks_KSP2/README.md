# OrbitWorks KSP2

Plans de **fusées / Starlink / Starship / rovers** pour **Kerbal Space Program 2**, avec IDs de pièces stock, blueprints VAB, et viewer 3D procédural.

## Assets 3D du jeu (important)

Les meshes et textures officiels KSP2 sont **propriétaires**. OrbitWorks **ne les extrait pas et ne les redistribue pas**.

- La vue 3D = **reconstruction procédurale** (silhouette Starship, bus Starlink, fusées, rovers) avec glow moteurs / fond étoilé.
- Pour jouer avec les **vrais modèles du jeu** : reconstruis chaque craft dans le **VAB** en suivant le blueprint (noms affichés stock + checklist par rôle).

## Lancer

```bash
cd OrbitWorks_KSP2
./GO_OrbitWorks.sh
# → http://127.0.0.1:8777/
```

Ou :

```bash
python3 python/generate_crafts.py
python3 python/web_server.py
```

Windows : `GO_OrbitWorks.bat`

## Contenu (67 crafts)

| Catégorie | Exemples |
|-----------|----------|
| **Starlink** ×26 | LEO dense, SSO, polar, GTO, Mun/Minmus relays |
| **Starship** ×12 | Crew, cargo, tanker, HLS, depot, rescue, Eve/Jool |
| **Fusées** ×18 | Mun → Eeloo, station core, shuttles |
| **Rovers** ×7 | Mun, Duna, Eve, Laythe, Ike, Vall |
| **Comms / Data** ×4 | GEO, Mun, LEO science |

## UI atelier

- Onglets + chips destinations + recherche
- Tri (nom / masse / Δv / pièces)
- Checklist pièces collée au HUD (noms jeu)
- Copier checklist, blueprint Markdown, wireframe, auto-rotate
- Raccourcis : `←` `→` crafts, `W` wireframe, `R` rotate

## Import dans le vrai jeu

```bash
python3 python/install_to_ksp2.py
```

Cible typique Windows :

`%USERPROFILE%\AppData\LocalLow\Intercept Games\Kerbal Space Program 2\OrbitWorks_Import\`

1. Ouvre le `.md` blueprint
2. Dans le VAB, cherche chaque **nom affiché**
3. Assemble selon l’ordre / checklist par rôle
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

Édite `data/craft_recipes.json` puis :

```bash
python3 python/generate_crafts.py
```
