from abc import ABC, abstractmethod
from typing import Tuple
from core.Individu import individu
import numpy as np


class Crossover(ABC):
    """
    Classe abstraite de crossover
    """

    def __init__(self):
        pass

    @abstractmethod
    @staticmethod
    def crossover(parent1: individu, parent2: individu) -> Tuple[individu, individu]:
        """
        Fonction qui prend 2 individus (parents) et effectue le crossover pour obtenir
        deux nouveaux individus (enfants).
        Les coordonnées des parents doivent être déjà codées.
        Retourne deux nouveaux individus avec des coordonnées codées issues du crossover.
        """
        pass


class MultiPointCrossover(Crossover):
    """
    Crossover multipoint avec un nombre fixe de points de coupure.
    """

    def __init__(self, nb_points: int = 2):
        super().__init__()
        self.nb_points = nb_points

    def crossover(self, parent1: individu, parent2: individu) -> Tuple[individu, individu]:
        encoded1 = parent1.coordonnees.coordonnees_codees
        encoded2 = parent2.coordonnees.coordonnees_codees

        # Check lengths match
        if len(encoded1) != len(encoded2):
            raise ValueError("Les coordonnées codées des parents doivent avoir la même longueur")

        length = len(encoded1)
        points = sorted(np.random.choice(range(1, length), self.nb_points, replace=False))

        # Create masks for crossover segments
        # Even segments from parent1, odd segments from parent2 (and vice versa)
        child1_bits = []
        child2_bits = []

        last = 0
        take_from_parent1 = True
        for point in points + [length]:
            if take_from_parent1:
                child1_bits.extend(encoded1[last:point])
                child2_bits.extend(encoded2[last:point])
            else:
                child1_bits.extend(encoded2[last:point])
                child2_bits.extend(encoded1[last:point])
            take_from_parent1 = not take_from_parent1
            last = point

        # Create new coordonnees and individus for children
        from core.Coordonnees import coordonnees

        child1_coord = coordonnees(np.array(parent1.coordonnees.coordonnees))  # copy real coords if needed
        child2_coord = coordonnees(np.array(parent2.coordonnees.coordonnees))

        # Set encoded coordinates to new crossed over bits
        child1_coord.coordonnees_codees = np.array(child1_bits)
        child2_coord.coordonnees_codees = np.array(child2_bits)

        # Create new individu objects (ids can be None or new ids)
        child1 = individu(id=None, coordonnees=child1_coord)
        child2 = individu(id=None, coordonnees=child2_coord)

        return child1, child2


# === Test ===
if __name__ == "__main__":
    import numpy as np
    from core.Coordonnees import coordonnees

    # Fake parents with codified bits
    parent1_coord = coordonnees(np.array([1.5, -2.3]))
    parent1_coord.coordonnees_codees = np.array([1, 0, 1, 1, 0, 0, 1, 0])
    parent2_coord = coordonnees(np.array([-0.5, 3.3]))
    parent2_coord.coordonnees_codees = np.array([0, 1, 0, 0, 1, 1, 0, 1])

    from core.Individu import individu

    parent1 = individu(1, parent1_coord)
    parent2 = individu(2, parent2_coord)

    crossover = MultiPointCrossover(nb_points=2)
    child1, child2 = crossover.crossover(parent1, parent2)

    print("Parent 1 bits:", parent1.coordonnees.coordonnees_codees)
    print("Parent 2 bits:", parent2.coordonnees.coordonnees_codees)
    print("Child 1 bits: ", child1.coordonnees.coordonnees_codees)
    print("Child 2 bits: ", child2.coordonnees.coordonnees_codees)
