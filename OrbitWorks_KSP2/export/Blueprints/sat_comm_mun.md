# MunComm Relay Trio

**OrbitWorks ID:** `sat_comm_mun`
**Catégorie:** comms
**Type / sous-type:** satellite / comms
**Destination:** Mun
**Masse estimée:** 21.926 t
**Δv estimé (indicatif):** ~5200 m/s
**Tags:** comms, mun

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
| 3 | Probodobodyne HECS | `probe_1v_hecs` | core | 0.300 |
| 3 | RA-2 Relay Antenna | `antenna_ra2` | comms | 0.450 |
| 3 | HG-5 High Gain Antenna | `antenna_hg5` | comms | 0.210 |
| 12 | OX-STAT Photovoltaic Panels | `panel_oxstat` | power | 0.060 |
| 3 | Z-1k Battery | `battery_z1k` | power | 0.150 |
| 3 | 48-7S Spark | `engine_1v_methalox_spark` | sat | 0.390 |
| 6 | Oscar-B | `fueltank_0v_inline_methalox_oscar` | sat | 0.576 |
| 1 | LV-909 Terrier | `engine_1v_methalox_terrier` | transfer | 0.500 |
| 2 | FL-T400 | `fueltank_1v_inline_methalox_1x4` | transfer | 4.500 |
| 1 | TR-18A Stack Decoupler | `decoupler_1v_stack` | stage | 0.040 |
| 1 | LV-T30 Reliant | `engine_1v_methalox_reliant` | booster | 1.250 |
| 3 | FL-T800 | `fueltank_1v_inline_methalox_1x8` | booster | 13.500 |

## Par rôle (rapide VAB)

### core
- [ ] ×3 **Probodobodyne HECS** (`probe_1v_hecs`)

### comms
- [ ] ×3 **RA-2 Relay Antenna** (`antenna_ra2`)
- [ ] ×3 **HG-5 High Gain Antenna** (`antenna_hg5`)

### power
- [ ] ×12 **OX-STAT Photovoltaic Panels** (`panel_oxstat`)
- [ ] ×3 **Z-1k Battery** (`battery_z1k`)

### sat
- [ ] ×3 **48-7S Spark** (`engine_1v_methalox_spark`)
- [ ] ×6 **Oscar-B** (`fueltank_0v_inline_methalox_oscar`)

### transfer
- [ ] ×1 **LV-909 Terrier** (`engine_1v_methalox_terrier`)
- [ ] ×2 **FL-T400** (`fueltank_1v_inline_methalox_1x4`)

### stage
- [ ] ×1 **TR-18A Stack Decoupler** (`decoupler_1v_stack`)

### booster
- [ ] ×1 **LV-T30 Reliant** (`engine_1v_methalox_reliant`)
- [ ] ×3 **FL-T800** (`fueltank_1v_inline_methalox_1x8`)

## Ordre de montage suggéré (bas → haut)

1. Moteurs / boosters + réservoirs bas
2. Découpleurs / séparateurs
3. Étage supérieur + avionique
4. Payload (sats / cargo / rover)
5. Coiffe / aéro / ailerons Starship

## Notes

3 relais Mun.

_Généré 2026-09-14 20:52 UTC — OrbitWorks_
