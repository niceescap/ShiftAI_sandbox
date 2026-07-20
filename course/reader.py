"""Lecteur de profil : pré-calcule la table des pentes (%)."""
import json
import math
from config import DUREE_SIMULATION_SEC, DT

class ProfileReader:
    """Approche A : pré-calcul au chargement pour consommation O(1) au loop 1Hz."""

    def __init__(self, path="course/profile.json"):
        with open(path, "r") as f:
            data = json.load(f)
        self.sommets = data["sommets"]  # [[t_min, alt_m], ...]
        self.table_pentes = []  # indexé par seconde
        self._precalcul()

    def _precalcul(self):
        """Génère table_pentes[sec] en % de pente instantanée."""
        # Interpolation linéaire par minute, puis conversion en secondes
        # On calcule la pente entre points successifs
        for sec in range(int(DUREE_SIMULATION_SEC)):
            t_min = sec / 60.0
            pente_pct = self._interpole_pente(t_min)
            self.table_pentes.append(pente_pct)

    def _interpole_pente(self, t_min: float) -> float:
        # Trouver segment [t_i, t_i+1] contenant t_min
        pts = self.sommets
        for i in range(len(pts) - 1):
            t0, a0 = pts[i]
            t1, a1 = pts[i + 1]
            if t0 <= t_min <= t1:
                # Pente en % entre ces deux points
                delta_t = t1 - t0
                delta_a = a1 - a0
                if delta_t > 0:
                    # Altitude à t_min
                    ratio = (t_min - t0) / delta_t if delta_t > 0 else 0
                    alt_t = a0 + ratio * delta_a
                    # Pente instantanée approximée sur petit intervalle
                    # Pour simplifier : on retourne la pente du segment
                    return (delta_a / (delta_t * 60)) * 100  # % approximé (m/min → % simplifié)
        return 0.0

    def get_pente_pct(self, sec: int) -> float:
        if sec < len(self.table_pentes):
            return self.table_pentes[sec]
        return self.table_pentes[-1] if self.table_pentes else 0.0
