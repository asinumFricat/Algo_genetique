import numpy as np
from core.Individu import individu


class Mutation:
    """
    Classe qui permet d'effectuer une mutation sur un individu selon un certain taux de mutation
    """

    def __init__(self, taux_mutation: float):
        self.taux_mutation = taux_mutation

    def mutation(self, indiv: individu):
        """
        Effectue une mutation sur les coordonnées codées de l'individu.
        Chaque bit a une probabilité `taux_mutation` d'être inversé.
        Modifie l'individu en place.
        """
        encoded = indiv.coordonnees.coordonnees_codees
        if encoded is None:
            raise ValueError("L'individu doit avoir des coordonnées codées pour mutation")

        for i in range(len(encoded)):
            if np.random.rand() < self.taux_mutation:
                encoded[i] = 1 - encoded[i]  # Flip bit

        indiv.coordonnees.coordonnees_codees = encoded


# === Test ===
if __name__ == "__main__":
    from core.Coordonnees import coordonnees
    from core.Individu import individu
    np.random.seed(42)

    coord = coordonnees(np.array([3.3, -1.2]))
    coord.coordonnees_codees = np.array([1, 0, 1, 1, 0, 0, 1, 0])

    ind = individu(1, coord)
    mutation = Mutation(taux_mutation=0.3)

    print("Avant mutation :", ind.coordonnees.coordonnees_codees)
    mutation.mutation(ind)
    print("Après mutation:", ind.coordonnees.coordonnees_codees)
