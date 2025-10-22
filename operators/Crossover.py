from abc import ABC, abstractmethod
from typing import Tuple
from core.Individu import Individu


class Crossover(ABC):
    """
    Classe abstraite de crossover
    """

    def __init__(self):
        pass

    @abstractmethod
    @staticmethod
    def crossover(parent1: Individu, parent2: Individu) -> Tuple[Individu, Individu]:
        """
        Fonction qui prends 2 individus (les parents) et effectue le crossover pour obtenir
        deux nouveaux individus (les enfants).
        En supposant que les coordonnées des parents sont déjà encodées.
        On obtient alors des individus avec seulement des encoded_coordonnees pour l'instant
        """


class SimpleCrossover(Crossover):
    """
    Crossover le plus simple qui coupe en deux l'ADN  de manière aléatoire
    en mettant première partie un morceau de l'ADN du parent1 et en deuxième partie l'ADN
    du parent2 pour l'enfant 1 et l'inverse pour l'enfant2
    """

    @staticmethod
    def crossover(parent1: Individu, parent2: Individu) -> Tuple[Individu, Individu]:
        encoded1 = parent1.coordonnees.encoded_coord
        encoded2 = parent2.coordonnees.encoded_coord
        return
