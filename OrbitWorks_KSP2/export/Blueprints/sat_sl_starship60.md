# Starlink Starship Deploy ×60

**OrbitWorks ID:** `sat_sl_starship60`
**Catégorie:** starlink
**Type / sous-type:** satellite / starlink
**Destination:** Kerbin LEO
**Masse estimée:** 690.700 t
**Δv estimé (indicatif):** ~3400 m/s
**Tags:** starlink, starship, mega

## Important — KSP 2

KSP2 n'a pas d'import craft 1-clic stable comme KSP1.
Reconstruisez ce vaisseau dans le **VAB** avec les pièces stock ci-dessous
(noms affichés = ceux du jeu). Les meshes/textures restent ceux de votre installation.

### Astuce VAB

1. Ouvre le VAB → cherche chaque **Nom affiché** dans la barre de recherche.
2. Assemble bas → haut (boosters d'abord, payload en dernier).
3. Sauvegarde le craft dans ton dossier véhicules KSP2.
4. Les JSON `Vehicles/` sont des scaffolds expérimentaux — ne les copie pas comme crafts natifs.

## Checklist pièces (stock KSP2)

| Qty | Nom affiché (jeu) | ID interne | Rôle | Masse ligne (t) |
|----:|-------------------|------------|------|----------------:|
| 1 | Starship-K Heatshield Nose | `nosecone_3v_heatshield` | ship | 2.500 |
| 1 | Starship-K Cargo Bay | `body_starship_cargo` | ship | 4.000 |
| 1 | Constellation Dispenser x60 | `payload_dispenser_60` | payload | 1.200 |
| 60 | Starlink-K V2 Bus | `payload_starlink_v2` | sat | 19.200 |
| 60 | Gigantor XL Solar Array | `panel_gigantor` | sat | 18.000 |
| 60 | HG-5 High Gain Antenna | `antenna_hg5` | sat | 4.200 |
| 60 | Probodobodyne OKTO | `probe_1v_octo` | sat | 6.000 |
| 4 | Starship-K Elevon | `wing_starship_flap` | ship | 1.400 |
| 3 | S3 KS-25x4 / Rhino-class | `engine_3v_methalox_rhino` | ship | 27.000 |
| 2 | S3-14400 | `fueltank_3v_inline_methalox_1x4` | ship | 162.000 |
| 1 | TR-XL Stack Decoupler | `decoupler_3v_stack` | stage | 0.200 |
| 1 | SuperHeavy-K Booster Core | `body_superheavy` | booster | 120.000 |
| 9 | S3 KS-25 Vector | `engine_3v_methalox_vector` | booster | 36.000 |
| 2 | S4-25600 | `fueltank_3v_inline_methalox_1x8` | booster | 288.000 |
| 4 | Heavy Grid Fin | `gridfin_heavy` | booster | 1.000 |

## Par rôle (rapide VAB)

### ship
- [ ] ×1 **Starship-K Heatshield Nose** (`nosecone_3v_heatshield`)
- [ ] ×1 **Starship-K Cargo Bay** (`body_starship_cargo`)
- [ ] ×4 **Starship-K Elevon** (`wing_starship_flap`)
- [ ] ×3 **S3 KS-25x4 / Rhino-class** (`engine_3v_methalox_rhino`)
- [ ] ×2 **S3-14400** (`fueltank_3v_inline_methalox_1x4`)

### payload
- [ ] ×1 **Constellation Dispenser x60** (`payload_dispenser_60`)

### sat
- [ ] ×60 **Starlink-K V2 Bus** (`payload_starlink_v2`)
- [ ] ×60 **Gigantor XL Solar Array** (`panel_gigantor`)
- [ ] ×60 **HG-5 High Gain Antenna** (`antenna_hg5`)
- [ ] ×60 **Probodobodyne OKTO** (`probe_1v_octo`)

### stage
- [ ] ×1 **TR-XL Stack Decoupler** (`decoupler_3v_stack`)

### booster
- [ ] ×1 **SuperHeavy-K Booster Core** (`body_superheavy`)
- [ ] ×9 **S3 KS-25 Vector** (`engine_3v_methalox_vector`)
- [ ] ×2 **S4-25600** (`fueltank_3v_inline_methalox_1x8`)
- [ ] ×4 **Heavy Grid Fin** (`gridfin_heavy`)

## Ordre de montage suggéré (bas → haut)

1. Moteurs / boosters + réservoirs bas
2. Découpleurs / séparateurs
3. Étage supérieur + avionique
4. Payload (sats / cargo / rover)
5. Coiffe / aéro / ailerons Starship

## Notes

Déploiement Starlink depuis baie Starship-K + SuperHeavy.

_Généré 2026-09-15 08:35 UTC — OrbitWorks_
