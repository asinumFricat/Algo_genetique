from abc import ABC, abstractmethod
from typing import Tuple
from core.Individu import individu

class Crossover(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def crossover(self, parent1: individu, parent2: individu) -> Tuple[individu, individu]:
        pass


class SimpleCrossover(Crossover):
    def __init__(self, points_coupure=2):
        self.points_coupure = points_coupure

    def crossover(self, parent1: individu, parent2: individu) -> Tuple[individu, individu]:
        adn1 = parent1.coordonnees.coordonnees_codees
        adn2 = parent2.coordonnees.coordonnees_codees

        length = len(adn1)
        points = sorted(np.random.choice(range(1, length), self.points_coupure, replace=False))

        enfant1 = []
        enfant2 = []

        dernier = 0
        for i, point in enumerate(points + [length]):
            if i % 2 == 0:
                enfant1 += adn1[dernier:point]
                enfant2 += adn2[dernier:point]
            else:
                enfant1 += adn2[dernier:point]
                enfant2 += adn1[dernier:point]
            dernier = point

        # Create new individu objects with the crossed ADN
        coord1 = parent1.coordonnees.__class__(parent1.coordonnees.coordonnees)  # coords unchanged here
        coord2 = parent2.coordonnees.__class__(parent2.coordonnees.coordonnees)
        coord1.coordonnees_codees = enfant1
        coord2.coordonnees_codees = enfant2

        ind1 = individu(-1, coord1)  # ID to be assigned later
        ind2 = individu(-1, coord2)

        return ind1, ind2
