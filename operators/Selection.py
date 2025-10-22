from abc import ABC, abstractmethod

from core.Population import Population


class Selection(ABC):
    """
    Classe abstraite de sélection d'individus dans une population
    """

    def __init__(self, population: Population):
        self.population = population

    @abstractmethod
    # Oblige à avaoir une méthode selection dans les classes filles
    def selection(self):
        pass


class selection_tournoi(Selection):
    def __init__(self, population: Population):
        super().__init__(population)


class selection_roulette(Selection):
    def __init__(self, population: Population):
        super().__init__(population)
