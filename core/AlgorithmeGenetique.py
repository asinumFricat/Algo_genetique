from core.Population import population
from core.Individu import individu
from core.Coordonnees import coordonnees
from operators.Codage import codage_binaire
from operators.Crossover import SimpleCrossover
from operators.Mutation import Mutation
from operators.Selection import selection_tournoi, selection_roulette
import numpy as np


class AlgorithmeGenetique:
    """
    Classe principale de l'algorithme génétique
    """

    def __init__(
        self,
        taille_population: int = 50,
        taux_mutation: float = 0.01,
        dimension_variables: int = 3,
        taille_codage: int = 16,
        minimisation: bool = True,
        selection_type: str = "tournoi",  # 'tournoi' or 'roulette'
    ):
        self.taille_population = taille_population
        self.taux_mutation = taux_mutation
        self.dimension_variables = dimension_variables
        self.taille_codage = taille_codage
        self.minimisation = minimisation

        # Fenêtre de recherche: pour chaque coordonnée, here hardcoded as [-10, 10] for example
        self.bornes = [(-10, 10)] * self.dimension_variables

        # Codage
        self.codage = codage_binaire()

        # Population init
        self.population = self._init_population()

        # Operators
        self.mutation = Mutation(self.taux_mutation)
        if selection_type == "tournoi":
            self.selection = selection_tournoi(self.population, taille_tournoi=3, minimisation=self.minimisation)
        elif selection_type == "roulette":
            self.selection = selection_roulette(self.population, minimisation=self.minimisation)
        else:
            raise ValueError("Type de sélection inconnu")

        self.crossover = SimpleCrossover()

    def _init_population(self) -> population:
        individus = []
        for i in range(self.taille_population):
            coords = np.array([np.random.uniform(low, high) for (low, high) in self.bornes])
            coord_obj = coordonnees(coords)
            # Codage MantisseExposant binaire (to implement in codage_binaire)
            coord_obj.coordonnees_codees = self.codage.codage(coords)
            ind = individu(i, coord_obj)
            individus.append(ind)
        return population(individus)

    def evaluer_performance(self, ind: individu):
        """
        Évalue la fonction objectif (benchmark) pour un individu donné.
        Pour l'exemple, on utilise une simple fonction sphere : sum(x_i^2)
        """
        x = ind.coordonnees.coordonnees
        f = np.sum(x ** 2)
        ind.performance = f if self.minimisation else -f

    def evaluer_population(self):
        for ind in self.population.liste_individus:
            self.evaluer_performance(ind)

    def run(self, generations: int = 100):
        self.evaluer_population()
        for gen in range(generations):
            # Sélection
            parent1, parent2 = self.selection.selection()

            # Crossover
            enfant1, enfant2 = self.crossover.crossover(parent1, parent2)

            # Mutation
            self.mutation.mutation(enfant1)
            self.mutation.mutation(enfant2)

            # Evaluer enfants
            self.evaluer_performance(enfant1)
            self.evaluer_performance(enfant2)

            # Choisir 2 parmi Père, Mère, Enfant1, Enfant2
            candidats = [parent1, parent2, enfant1, enfant2]
            # Trie selon performance (selon minimisation/maximisation)
            candidats.sort(key=lambda ind: ind.performance, reverse=not self.minimisation)
            meilleurs = candidats[:2]

            # Remplacer dans la population (ex: retirer parents, ajouter meilleurs enfants)
            self.population.retirer([parent1, parent2])
            self.population.ajouter(meilleurs)

            # Evaluer population again to update selection pool
            self.evaluer_population()

            print(f"Génération {gen+1}, Meilleur: {meilleurs[0].performance}")

        # Retourner le meilleur individu final
        self.population.liste_individus.sort(key=lambda ind: ind.performance, reverse=not self.minimisation)
        return self.population.liste_individus[0]


if __name__ == "__main__":
    ag = AlgorithmeGenetique(
        taille_population=50,
        taux_mutation=0.01,
        dimension_variables=3,
        taille_codage=16,
        minimisation=True,
        selection_type="tournoi",
    )
    meilleur = ag.run(generations=50)
    print(f"Meilleur individu trouvé: {meilleur}")
