# Starlink Minmus Node ×8

**OrbitWorks ID:** `sat_sl_minmus`
**Catégorie:** starlink
**Type / sous-type:** satellite / starlink
**Destination:** Minmus
**Masse estimée:** 91.610 t
**Δv estimé (indicatif):** ~4800 m/s
**Tags:** starlink, extended

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
| 1 | Constellation Dispenser x24 | `payload_dispenser_24` | payload | 0.800 |
| 8 | Starlink-K Flat Bus | `payload_starlink_bus` | sat | 2.080 |
| 2 | Gigantor XL Solar Array | `panel_gigantor` | sat | 0.600 |
| 2 | Communotron 16 | `antenna_comm16` | sat | 0.010 |
| 2 | Probodobodyne OKTO | `probe_1v_octo` | sat | 0.200 |
| 2 | Z-100 Rechargeable Battery | `battery_z100` | sat | 0.010 |
| 1 | LV-909 Terrier | `engine_1v_methalox_terrier` | upper | 0.500 |
| 2 | FL-T800 | `fueltank_1v_inline_methalox_1x8` | upper | 9.000 |
| 1 | TR-38-D Stack Decoupler | `decoupler_2v_stack` | stage | 0.080 |
| 1 | RE-M3 Mainsail | `engine_2v_methalox_mainsail` | booster | 6.000 |
| 2 | X200-64 | `fueltank_2v_inline_methalox_1x8` | booster | 72.000 |
| 1 | AE-FF2 Airstream Protective Shell | `fairing_2v` | aero | 0.250 |
| 4 | Delta-Deluxe Winglet | `fin_delta_deluxe` | aero | 0.080 |

## Par rôle (rapide VAB)

### payload
- [ ] ×1 **Constellation Dispenser x24** (`payload_dispenser_24`)

### sat
- [ ] ×8 **Starlink-K Flat Bus** (`payload_starlink_bus`)
- [ ] ×2 **Gigantor XL Solar Array** (`panel_gigantor`)
- [ ] ×2 **Communotron 16** (`antenna_comm16`)
- [ ] ×2 **Probodobodyne OKTO** (`probe_1v_octo`)
- [ ] ×2 **Z-100 Rechargeable Battery** (`battery_z100`)

### upper
- [ ] ×1 **LV-909 Terrier** (`engine_1v_methalox_terrier`)
- [ ] ×2 **FL-T800** (`fueltank_1v_inline_methalox_1x8`)

### stage
- [ ] ×1 **TR-38-D Stack Decoupler** (`decoupler_2v_stack`)

### booster
- [ ] ×1 **RE-M3 Mainsail** (`engine_2v_methalox_mainsail`)
- [ ] ×2 **X200-64** (`fueltank_2v_inline_methalox_1x8`)

### aero
- [ ] ×1 **AE-FF2 Airstream Protective Shell** (`fairing_2v`)
- [ ] ×4 **Delta-Deluxe Winglet** (`fin_delta_deluxe`)

## Ordre de montage suggéré (bas → haut)

1. Moteurs / boosters + réservoirs bas
2. Découpleurs / séparateurs
3. Étage supérieur + avionique
4. Payload (sats / cargo / rover)
5. Coiffe / aéro / ailerons Starship

## Notes

Nœuds glace Minmus — faible Δv.

_Généré 2026-09-14 20:52 UTC — OrbitWorks_
