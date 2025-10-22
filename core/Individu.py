from core.Coordonnees import coordonnees
from operators.Codage import Codage

class individu:
    def __init__(self, id: int, coordonnees: coordonnees, codage: Codage = None):
        self.id = id  # Identifiant unique
        self.coordonnees = coordonnees
        self.elite = False  # Pour d'éventuelles stratégies d'élitisme
        self.fitness = None  # Calculée selon la fonction de performance (benchmark)
        
        if codage:
            # Codage automatique dès l'initialisation
            codage.code(self.coordonnees)

    def __str__(self):
        return (f"ID : {self.id}, "
                f"coordonnées : {self.coordonnees.coordonnees}, "
                f"codées : {self.coordonnees.coordonnees_codees}, "
                f"fitness : {self.fitness}, elite : {self.elite}")

# === Test ===
if __name__ == "__main__":
    import numpy as np
    from core.Coordonnees import coordonnees
    from operators.Codage import CodageMantisseExposant

    # Create raw coordinates
    coords = coordonnees(np.array([1.5, -3.2]))

    # Create coder
    coder = CodageMantisseExposant(bits_per_var=16, exponent_bits=5)

    # Create individual with automatic codage
    ind = individu(1, coords, codage=coder)
    print(ind)
