from core.Individu import individu
import numpy as np


class Mutation:
    def __init__(self, taux_mutation: float):
        self.taux_mutation = taux_mutation

    def mutation(self, individu: individu):
        """
        Mutate bits in individu.coordonnees.coordonnees_codees with probability taux_mutation
        """
        bits = individu.coordonnees.coordonnees_codees.copy()
        for i in range(len(bits)):
            if np.random.rand() < self.taux_mutation:
                bits[i] = 1 - bits[i]  # flip bit

        individu.coordonnees.coordonnees_codees = bits
        return individu


if __name__ == "__main__":
    import numpy as np
    from core.Coordonnees import coordonnees
    from core.Individu import individu

    c = coordonnees(np.array([1, 2]))
    c.coordonnees_codees = np.array([1, 0, 1, 0, 1, 0])
    ind = individu(1, c)

    mutation = Mutation(taux_mutation=0.1)
    mutated = mutation.mutation(ind)
    print("Original:", c.coordonnees_codees)
    print("Mutated: ", mutated.coordonnees.coordonnees_codees)
