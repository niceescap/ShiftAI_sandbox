"""Moteur physique simplifié - boucle 1Hz non bloquante."""
import math
from config import (
    PUISSANCE_CYCLISTE_W, MASSE_TOTALE_KG, GRAVITE,
    CDA, RHO_AIR, CRR, CIRCONFERENCE_ROUE_M,
    DT, DUREE_SIMULATION_SEC
)
from derailer import Derailer
from course.reader import ProfileReader

class Simulator:
    """Simulateur physique simplifié (coefficients fixes sauf pente)."""

    def __init__(self):
        self.v_kmh = 0.0  # vitesse en km/h (pour télémesure)
        self.v_mps = 0.0  # vitesse en m/s (pour physique)
        self.derailer = Derailer()
        self.profile_reader = ProfileReader()
        self.timestamp = 0.0

    def tick(self, sec: int):
        """Un pas du loop 1Hz."""
        # 1. Pente depuis le profil (variable dynamique)
        pente_pct = self.profile_reader.get_pente_pct(sec)
        theta = math.atan(pente_pct / 100.0)

        # 2. Résistances
        F_pente = MASSE_TOTALE_KG * GRAVITE * math.sin(theta)
        F_roulement = MASSE_TOTALE_KG * GRAVITE * CRR
        F_aero = 0.5 * RHO_AIR * CDA * (self.v_mps ** 2)
        F_resistance = F_pente + F_roulement + F_aero

        # 3. Propulsion (puissance constante 250W)
        if self.v_mps > 0.1:
            F_propulsion = PUISSANCE_CYCLISTE_W / self.v_mps
        else:
            F_propulsion = PUISSANCE_CYCLISTE_W / 0.5  # démarrage lent

        # 4. Inertie (intégration Euler)
        accel = (F_propulsion - F_resistance) / MASSE_TOTALE_KG
        self.v_mps += accel * DT
        if self.v_mps < 0.05:
            self.v_mps = 0.05  # vitesse minimale

        # 5. Mise à jour vitesse km/h
        self.v_kmh = self.v_mps * 3.6

        # 6. Cadence calculée depuis vitesse + ratio actuel
        ratio = self.derailer.get_ratio()
        cadence = (self.v_kmh * 1000) / (ratio * CIRCONFERENCE_ROUE_M * 60)

        self.timestamp = float(sec)
        return {
            "timestamp": self.timestamp,
            "speed_kmh": round(self.v_kmh, 2),
            "cadence_rpm": round(cadence, 1),
            "current_cog": self.derailer.get_index(),
            "pente_pct": round(pente_pct, 1),
        }

    def set_current_cog(self, index: int):
        """Réception du contrôleur : mise à jour immédiate du pignon."""
        self.derailer.set_current_cog(index)
        # La vitesse reste continue (v_mps non modifié)
        # La cadence sera recalculée au prochain tick avec le nouveau ratio.
