"""Registre interne du dérailleur. Reçoit current_cog uniquement."""
from config import CASSETTE, PIGNON_INITIAL_INDEX

class Derailer:
    def __init__(self):
        self.index = PIGNON_INITIAL_INDEX  # 5 -> 17T
        self.cog = CASSETTE[self.index]

    def set_current_cog(self, index: int):
        """Le simulateur reçoit uniquement current_cog de l'algorithme."""
        if 0 <= index < len(CASSETTE):
            self.index = index
            self.cog = CASSETTE[index]
        # Si hors bornes, on ignore (anti-rebond logiciel implicite)

    def get_index(self) -> int:
        return self.index

    def get_cog(self) -> int:
        return self.cog

    def get_ratio(self) -> float:
        return 40.0 / self.cog
