from abc import ABC, abstractmethod
from typing import Tuple
from core.Individu import individu
import numpy as np


class Crossover(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def crossover(self, parent1: individu, parent2: individu) -> Tuple[individu, individu]:
        """
        Effectue le crossover entre deux individus (parents)
        et retourne deux nouveaux individus (enfants).
        """
        pass


class MultiPointCrossover(Crossover):
    def __init__(self, n_points=2):
        super().__init__()
        self.n_points = n_points  # nombre fixe de points de coupure

    def crossover(self, parent1: individu, parent2: individu) -> Tuple[individu, individu]:
        encoded1 = parent1.coordonnees.coordonnees_codees
        encoded2 = parent2.coordonnees.coordonnees_codees

        length = len(encoded1)
        if length != len(encoded2):
            raise ValueError("Les deux parents doivent avoir le même nombre de bits encodés.")

        # Choisir n_points coupures distinctes et triées
        points = np.sort(np.random.choice(range(1, length), self.n_points, replace=False))

        child1_bits = []
        child2_bits = []

        # Faire l'alternance des segments entre parents
        last_point = 0
        toggle = True
        for point in list(points) + [length]:
            if toggle:
                child1_bits.extend(encoded1[last_point:point])
                child2_bits.extend(encoded2[last_point:point])
            else:
                child1_bits.extend(encoded2[last_point:point])
                child2_bits.extend(encoded1[last_point:point])
            toggle = not toggle
            last_point = point

        # Créer nouveaux individus (sans id, id à gérer dans Population ou Algorithme)
        from core.Coordonnees import coordonnees
        child1_coord = coordonnees(np.array([]))  # coordonnées à remplir dans autre logique
        child2_coord = coordonnees(np.array([]))
        child1_coord.coordonnees_codees = np.array(child1_bits)
        child2_coord.coordonnees_codees = np.array(child2_bits)

        child1 = individu(-1, child1_coord)  # id à définir proprement
        child2 = individu(-1, child2_coord)

        return child1, child2


if __name__ == "__main__":
    import numpy as np
    from core.Coordonnees import coordonnees
    from core.Individu import individu

    # Exemple simple
    c1 = coordonnees(np.array([1.0, 2.0]))
    c2 = coordonnees(np.array([3.0, 4.0]))
    c1.coordonnees_codees = np.array([1, 0, 1, 0, 1, 0])
    c2.coordonnees_codees = np.array([0, 1, 0, 1, 0, 1])
    p1 = individu(1, c1)
    p2 = individu(2, c2)

    crossover = MultiPointCrossover(n_points=2)
    child1, child2 = crossover.crossover(p1, p2)

    print("Child1:", child1.coordonnees.coordonnees_codees)
    print("Child2:", child2.coordonnees.coordonnees_codees)
