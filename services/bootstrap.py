"""Unified bootstrap — one load sequence for the iCUE interface."""

from dataclasses import dataclass
from typing import Callable, Optional

from core.engine import MacroManager
from services.engine_proxy import EngineProxy
from services.profile_manager import ProfileManager
from services.sidecar_api import SidecarAPI


ProgressCallback = Callable[[int, str], None]


@dataclass
class BootContext:
    manager: MacroManager
    proxy: EngineProxy
    profiles: ProfileManager
    sidecar: SidecarAPI


def _report(cb: Optional[ProgressCallback], percent: int, message: str):
    if cb:
        cb(percent, message)


def bootstrap(progress: Optional[ProgressCallback] = None) -> BootContext:
    """Initialize engine, profiles, and sidecar in one sequence."""
    _report(progress, 5, "Initialisation du moteur Win32…")
    manager = MacroManager()

    _report(progress, 25, "Connexion des macros souris / clavier…")
    proxy = EngineProxy(manager)

    _report(progress, 45, "Chargement du profil…")
    profiles = ProfileManager()
    profiles.load("default")
    profiles.apply_to_engine(manager)

    _report(progress, 65, "Démarrage API Sidecar (port 17840)…")
    sidecar = SidecarAPI(proxy)
    sidecar.start()

    _report(progress, 85, "Préparation interface iCUE…")

    return BootContext(
        manager=manager,
        proxy=proxy,
        profiles=profiles,
        sidecar=sidecar,
    )
