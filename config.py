"""Configuration du simulateur Fit Live."""
# Physique
PUISSANCE_CYCLISTE_W = 250.0
MASSE_TOTALE_KG = 75.0
GRAVITE = 9.81

# Résistances (coefficients fixes simplifiés)
CDA = 0.32
RHO_AIR = 1.2  # densité air simplifiée
CRR = 0.005   # coefficient roulement

# Transmission
PLATEAU_DENTS = 40
CASSETTE = [11, 12, 13, 14, 15, 17, 19, 21, 24, 28, 32, 36]
PIGNON_INITIAL_INDEX = 5  # 17T

# Roue 700
CIRCONFERENCE_ROUE_M = 2.105  # rayon ~668mm + pneu

# Simulation
DT = 1.0  # boucle 1 Hz
DUREE_SIMULATION_SEC = 300   # 5 minutes

# WebSocket / Serveur
WS_HOST = "0.0.0.0"
WS_PORT = 8765
HTTP_PORT = 8000
