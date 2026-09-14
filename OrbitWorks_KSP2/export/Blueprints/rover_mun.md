# Mun Scout Rover

**OrbitWorks ID:** `rover_mun`
**Catégorie:** rovers
**Type / sous-type:** rover / science
**Destination:** Mun
**Masse estimée:** 54.085 t
**Δv estimé (indicatif):** ~5200 m/s
**Tags:** rover, mun

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
| 1 | TR-2L Ruggedized Vehicle Wheel | `chassis_rover_tr2l` | chassis | 0.300 |
| 4 | RoveMax Model M1 | `wheel_rover_m1` | wheels | 0.200 |
| 1 | 2HOT Thermometer | `science_thermometer` | science | 0.005 |
| 1 | Communotron 16 | `antenna_comm16` | comms | 0.005 |
| 4 | OX-STAT Photovoltaic Panels | `panel_oxstat` | power | 0.020 |
| 1 | Z-1k Battery | `battery_z1k` | power | 0.050 |
| 4 | LT-1 Landing Struts | `landingleg_lt1` | lander | 0.200 |
| 1 | LV-909 Terrier | `engine_1v_methalox_terrier` | lander | 0.500 |
| 1 | FL-T200 | `fueltank_1v_inline_methalox_1x2` | lander | 1.125 |
| 1 | TR-18A Stack Decoupler | `decoupler_1v_stack` | stage | 0.040 |
| 1 | LV-909 Terrier | `engine_1v_methalox_terrier` | transfer | 0.500 |
| 2 | FL-T800 | `fueltank_1v_inline_methalox_1x8` | transfer | 9.000 |
| 1 | TR-18A Stack Decoupler | `decoupler_1v_stack` | stage | 0.040 |
| 1 | RE-M3 Mainsail | `engine_2v_methalox_mainsail` | booster | 6.000 |
| 2 | X200-32 | `fueltank_2v_inline_methalox_1x4` | booster | 36.000 |

## Par rôle (rapide VAB)

### core
- [ ] ×1 **Probodobodyne HECS** (`probe_1v_hecs`)

### chassis
- [ ] ×1 **TR-2L Ruggedized Vehicle Wheel** (`chassis_rover_tr2l`)

### wheels
- [ ] ×4 **RoveMax Model M1** (`wheel_rover_m1`)

### science
- [ ] ×1 **2HOT Thermometer** (`science_thermometer`)

### comms
- [ ] ×1 **Communotron 16** (`antenna_comm16`)

### power
- [ ] ×4 **OX-STAT Photovoltaic Panels** (`panel_oxstat`)
- [ ] ×1 **Z-1k Battery** (`battery_z1k`)

### lander
- [ ] ×4 **LT-1 Landing Struts** (`landingleg_lt1`)
- [ ] ×1 **LV-909 Terrier** (`engine_1v_methalox_terrier`)
- [ ] ×1 **FL-T200** (`fueltank_1v_inline_methalox_1x2`)

### stage
- [ ] ×1 **TR-18A Stack Decoupler** (`decoupler_1v_stack`)
- [ ] ×1 **TR-18A Stack Decoupler** (`decoupler_1v_stack`)

### transfer
- [ ] ×1 **LV-909 Terrier** (`engine_1v_methalox_terrier`)
- [ ] ×2 **FL-T800** (`fueltank_1v_inline_methalox_1x8`)

### booster
- [ ] ×1 **RE-M3 Mainsail** (`engine_2v_methalox_mainsail`)
- [ ] ×2 **X200-32** (`fueltank_2v_inline_methalox_1x4`)

## Ordre de montage suggéré (bas → haut)

1. Moteurs / boosters + réservoirs bas
2. Découpleurs / séparateurs
3. Étage supérieur + avionique
4. Payload (sats / cargo / rover)
5. Coiffe / aéro / ailerons Starship

## Notes

Rover Mun + lander.

_Généré 2026-09-14 20:52 UTC — OrbitWorks_
