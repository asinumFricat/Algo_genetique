from abc import ABC, abstractmethod
from core.Population import population
import numpy as np


class Selection(ABC):
    def __init__(self, population: population):
        self.population = population

    @abstractmethod
    def selection(self):
        """
        Retourne une liste de deux individus sélectionnés pour crossover
        """
        pass


class selection_tournoi(Selection):
    def __init__(self, population: population, taille_tournoi=3):
        super().__init__(population)
        self.taille_tournoi = taille_tournoi

    def selection(self):
        """
        Sélection par tournoi: choisir 'taille_tournoi' individus aléatoires et retourner les deux meilleurs
        Ici, on suppose qu'on a un attribut 'performance' sur individu (à intégrer selon f(x))
        """
        if len(self.population.liste_individus) < self.taille_tournoi:
            raise ValueError("Population trop petite pour tournoi")

        candidats = np.random.choice(self.population.liste_individus, self.taille_tournoi, replace=False)
        # Trier par performance (supposons que performance est un float, plus petit meilleur si minimisation)
        sorted_candidats = sorted(candidats, key=lambda ind: getattr(ind, "performance", float('inf')))
        # Retourne les 2 meilleurs
        return sorted_candidats[0], sorted_candidats[1]


class selection_roulette(Selection):
    def __init__(self, population: population):
        super().__init__(population)

    def selection(self):
        """
        Sélection par roulette proportionnelle à la performance
        Ici on suppose que performance est positive et que l'on minimise donc on inverse
        """
        individus = self.population.liste_individus
        perf = np.array([getattr(ind, "performance", 0) for ind in individus])

        # Pour minimisation, convertir performances en "scores" positifs plus élevés meilleurs
        max_perf = np.max(perf)
        scores = max_perf - perf + 1e-6  # éviter zéro

        proba = scores / np.sum(scores)

        parents_indices = np.random.choice(len(individus), size=2, replace=False, p=proba)
        return individus[parents_indices[0]], individus[parents_indices[1]]


if __name__ == "__main__":
    # Test simple
    from core.Coordonnees import coordonnees
    from core.Individu import individu
    from core.Population import population

    import numpy as np

    c1 = coordonnees(np.array([1, 2]))
    c2 = coordonnees(np.array([3, 4]))
    ind1 = individu(1, c1)
    ind2 = individu(2, c2)

    ind1.performance = 10
    ind2.performance = 5

    pop = population([ind1, ind2])
    selection = selection_tournoi(pop, taille_tournoi=2)
    p1, p2 = selection.selection()
    print(f"Tournoi selection: {p1.id}, {p2.id}")

    selection_r = selection_roulette(pop)
    p1, p2 = selection_r.selection()
    print(f"Roulette selection: {p1.id}, {p2.id}")
