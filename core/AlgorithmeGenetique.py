from operators import Codage, Crossover, Mutation, Selection
from core import Population


class AlgorithmeGenetique:
    """
    Classe principale de l'algorithme génétique
    """

    def __init__(
        self,
        population: Population,
        codage: Codage,
        crossover: Crossover,
        mutation: Mutation,
        selection: Selection,
    ):
        self.population = population
        self.codage = codage
        self.crossover = crossover
        self.mutation = mutation
        self.selection = selection
