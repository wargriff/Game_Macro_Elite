# CommSat GEO Kerbin

**OrbitWorks ID:** `sat_comm_geo`
**Catégorie:** comms
**Type / sous-type:** satellite / comms
**Destination:** Kerbin GTO
**Masse estimée:** 22.040 t
**Δv estimé (indicatif):** ~4200 m/s
**Tags:** comms, geo

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
| 1 | Comm Relay Hub | `payload_relay_hub` | payload | 0.200 |
| 1 | RA-15 Relay Antenna | `antenna_ra15` | comms | 0.300 |
| 2 | HG-55 | `antenna_hg55` | comms | 0.150 |
| 2 | Gigantor XL Solar Array | `panel_gigantor` | power | 0.600 |
| 1 | Z-4k Battery | `battery_z4k` | power | 0.200 |
| 4 | RV-105 RCS Thruster Block | `rcs_rv105` | control | 0.200 |
| 2 | Stratus-V Roundified Monopropellant Tank | `rcs_tank_str` | control | 0.150 |
| 1 | LV-909 Terrier | `engine_1v_methalox_terrier` | upper | 0.500 |
| 2 | FL-T400 | `fueltank_1v_inline_methalox_1x4` | upper | 4.500 |
| 1 | TR-18A Stack Decoupler | `decoupler_1v_stack` | stage | 0.040 |
| 1 | LV-T45 Swivel | `engine_1v_methalox_swivel` | booster | 1.500 |
| 3 | FL-T800 | `fueltank_1v_inline_methalox_1x8` | booster | 13.500 |
| 1 | AE-FF1 Airstream Protective Shell | `fairing_1v` | aero | 0.100 |

## Par rôle (rapide VAB)

### core
- [ ] ×1 **Probodobodyne HECS** (`probe_1v_hecs`)

### payload
- [ ] ×1 **Comm Relay Hub** (`payload_relay_hub`)

### comms
- [ ] ×1 **RA-15 Relay Antenna** (`antenna_ra15`)
- [ ] ×2 **HG-55** (`antenna_hg55`)

### power
- [ ] ×2 **Gigantor XL Solar Array** (`panel_gigantor`)
- [ ] ×1 **Z-4k Battery** (`battery_z4k`)

### control
- [ ] ×4 **RV-105 RCS Thruster Block** (`rcs_rv105`)
- [ ] ×2 **Stratus-V Roundified Monopropellant Tank** (`rcs_tank_str`)

### upper
- [ ] ×1 **LV-909 Terrier** (`engine_1v_methalox_terrier`)
- [ ] ×2 **FL-T400** (`fueltank_1v_inline_methalox_1x4`)

### stage
- [ ] ×1 **TR-18A Stack Decoupler** (`decoupler_1v_stack`)

### booster
- [ ] ×1 **LV-T45 Swivel** (`engine_1v_methalox_swivel`)
- [ ] ×3 **FL-T800** (`fueltank_1v_inline_methalox_1x8`)

### aero
- [ ] ×1 **AE-FF1 Airstream Protective Shell** (`fairing_1v`)

## Ordre de montage suggéré (bas → haut)

1. Moteurs / boosters + réservoirs bas
2. Découpleurs / séparateurs
3. Étage supérieur + avionique
4. Payload (sats / cargo / rover)
5. Coiffe / aéro / ailerons Starship

## Notes

Relais haute orbite.

_Généré 2026-09-14 21:28 UTC — OrbitWorks_
