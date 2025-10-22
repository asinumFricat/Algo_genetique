from abc import ABC, abstractmethod
import numpy as np
from core.Population import population
from core.Individu import individu


class Selection(ABC):
    """
    Classe abstraite de sélection d'individus dans une population
    """

    def __init__(self, population: population):
        self.population = population

    @abstractmethod
    def selection(self) -> tuple[individu, individu]:
        """
        Retourne deux individus sélectionnés pour le crossover.
        """
        pass


class selection_tournoi(Selection):
    """
    Sélection par tournoi: Choisit aléatoirement un sous-ensemble de la population,
    puis prend le meilleur (selon performance) comme parent.
    """

    def __init__(self, population: population, taille_tournoi: int = 3, minimisation: bool = True):
        super().__init__(population)
        self.taille_tournoi = taille_tournoi
        self.minimisation = minimisation  # True = minimiser, False = maximiser

    def selection(self) -> tuple[individu, individu]:
        def meilleur_tournoi():
            participants = np.random.choice(self.population.liste_individus, self.taille_tournoi, replace=False)
            # Chaque individu doit avoir un attribut performance calculé à l'avance
            if self.minimisation:
                meilleur = min(participants, key=lambda ind: ind.performance)
            else:
                meilleur = max(participants, key=lambda ind: ind.performance)
            return meilleur

        parent1 = meilleur_tournoi()
        parent2 = meilleur_tournoi()
        while parent2 == parent1:
            parent2 = meilleur_tournoi()

        return parent1, parent2


class selection_roulette(Selection):
    """
    Sélection par roulette: probabilité proportionnelle à la performance (ajustée pour minimisation/maximisation)
    """

    def __init__(self, population: population, minimisation: bool = True):
        super().__init__(population)
        self.minimisation = minimisation

    def selection(self) -> tuple[individu, individu]:
        performances = np.array([ind.performance for ind in self.population.liste_individus])
        if self.minimisation:
            # Convert minimization scores to positive fitness (higher fitness better)
            max_perf = np.max(performances)
            fitness = max_perf - performances + 1e-6  # Avoid zero probability
        else:
            fitness = performances - np.min(performances) + 1e-6

        probabilities = fitness / np.sum(fitness)

        parent1 = np.random.choice(self.population.liste_individus, p=probabilities)
        parent2 = np.random.choice(self.population.liste_individus, p=probabilities)
        while parent2 == parent1:
            parent2 = np.random.choice(self.population.liste_individus, p=probabilities)

        return parent1, parent2


# === Test ===
if __name__ == "__main__":
    import numpy as np
    from core.Coordonnees import coordonnees
    from core.Individu import individu
    from core.Population import population

    # Create dummy individuals with performances
    coords = [coordonnees(np.array([i, i * 2])) for i in range(5)]
    for i, c in enumerate(coords):
        c.coordonnees_codees = np.array([0, 1] * 4)
    inds = [individu(i, c) for i, c in enumerate(coords)]
    # Assign fake performance (lower is better)
    for i, ind in enumerate(inds):
        ind.performance = float(i)  # 0 best, 4 worst

    pop = population(inds)

    sel_tournoi = selection_tournoi(pop, taille_tournoi=3, minimisation=True)
    sel_roul = selection_roulette(pop, minimisation=True)

    p1, p2 = sel_tournoi.selection()
    print(f"Tournoi sélection: {p1.id}, {p2.id}")

    p1, p2 = sel_roul.selection()
    print(f"Roulette sélection: {p1.id}, {p2.id}")
