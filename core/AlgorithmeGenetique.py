from operators import Codage, Crossover, Mutation, Selection, Performance
from core import Population


class AlgorithmeGenetique:
    """
    Classe principale de l'algorithme génétique
    """

    def __init__(self, population: Population, codage: Codage, crossover: Crossover, mutation: Mutation, selection: Selection, performance: Performance):
        self.population = population
        self.codage = codage
        self.crossover = crossover
        self.mutation = mutation
        self.selection = selection
        self.performance = performance

    def fonctionnement(self):
        while True :
            parents = self.selection.selection(population)
            enfants = self.crossover.croise(parents)
            enfants = self.mutation.mute(enfants)
            self.population.retire(parents)
            self.population.ajoute(self.performance.selectionNaturelle([enfants, parents]))



         


if __name__ == "__main__" : 

    #Initialisation 
    population = Population()
    codage = Codage()
    crossover = Crossover()
    mutation = Mutation()
    selection = Selection()
    performance = Performance()

    algo = AlgorithmeGenetique(population, codage, mutation, selection, performance)
    algo.fonctionnement()
