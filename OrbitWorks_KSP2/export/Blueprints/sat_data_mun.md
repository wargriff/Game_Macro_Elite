# MunScan DataSat

**OrbitWorks ID:** `sat_data_mun`
**Catégorie:** data
**Type / sous-type:** satellite / data
**Destination:** Mun
**Masse estimée:** 16.210 t
**Δv estimé (indicatif):** ~5200 m/s
**Tags:** data, mun

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
| 1 | Probodobodyne HECS | `probe_1v_hecs` | core | 0.100 |
| 1 | Orbital Data Core | `payload_data_core` | payload | 0.150 |
| 1 | SC-9001 Science Jr. | `science_sc9001` | science | 0.200 |
| 1 | HG-5 High Gain Antenna | `antenna_hg5` | comms | 0.070 |
| 1 | Gigantor XL Solar Array | `panel_gigantor` | power | 0.300 |
| 2 | Z-1k Battery | `battery_z1k` | power | 0.100 |
| 1 | LV-909 Terrier | `engine_1v_methalox_terrier` | transfer | 0.500 |
| 2 | FL-T400 | `fueltank_1v_inline_methalox_1x4` | transfer | 4.500 |
| 1 | TR-18A Stack Decoupler | `decoupler_1v_stack` | stage | 0.040 |
| 1 | LV-T30 Reliant | `engine_1v_methalox_reliant` | booster | 1.250 |
| 2 | FL-T800 | `fueltank_1v_inline_methalox_1x8` | booster | 9.000 |

## Par rôle (rapide VAB)

### core
- [ ] ×1 **Probodobodyne HECS** (`probe_1v_hecs`)

### payload
- [ ] ×1 **Orbital Data Core** (`payload_data_core`)

### science
- [ ] ×1 **SC-9001 Science Jr.** (`science_sc9001`)

### comms
- [ ] ×1 **HG-5 High Gain Antenna** (`antenna_hg5`)

### power
- [ ] ×1 **Gigantor XL Solar Array** (`panel_gigantor`)
- [ ] ×2 **Z-1k Battery** (`battery_z1k`)

### transfer
- [ ] ×1 **LV-909 Terrier** (`engine_1v_methalox_terrier`)
- [ ] ×2 **FL-T400** (`fueltank_1v_inline_methalox_1x4`)

### stage
- [ ] ×1 **TR-18A Stack Decoupler** (`decoupler_1v_stack`)

### booster
- [ ] ×1 **LV-T30 Reliant** (`engine_1v_methalox_reliant`)
- [ ] ×2 **FL-T800** (`fueltank_1v_inline_methalox_1x8`)

## Ordre de montage suggéré (bas → haut)

1. Moteurs / boosters + réservoirs bas
2. Découpleurs / séparateurs
3. Étage supérieur + avionique
4. Payload (sats / cargo / rover)
5. Coiffe / aéro / ailerons Starship

## Notes

Cartographie Mun.

_Généré 2026-09-14 21:28 UTC — OrbitWorks_
