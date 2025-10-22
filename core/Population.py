from Individu import individu

class population:
    def __init__(self, liste_individus : list[individu]):
        self.liste_individus = liste_individus if isinstance(liste_individus, list) else [liste_individus]

    def __str__(self):
        if len(self.liste_individus) == 0:
            return "La population est vide."
        else:
            x = (",\n".join(str(ind) for ind in self.liste_individus))
            return f"La population est composée des individus suivants : \n{x}"

    def ajouter(self, population : individu | list[individu]):
        if isinstance(population, list):
            self.liste_individus.extend(population)
        else:
            self.liste_individus.append(population)

    def retirer(self, population : individu | list[individu]):
        if isinstance(population, list):
            self.liste_individus = [x for x in self.liste_individus if x not in population]
        else:
            self.liste_individus.remove(population)

if __name__ == "__main__":
    import numpy as np
    from Coordonnees import coordonnees
    c1 = coordonnees(np.array([1,2]))
    c2 = coordonnees(np.array([3,4]))
    c2.coordonnees_codees = np.array([1, 0, 1, 0, 0, 1])
    i1 = individu(1, c1)
    i2 = individu(2, c2)
    pop = population(i1)
    print(pop)
    pop.ajouter(i2)
    print(pop)
    pop.retirer(i1)
    c2.coordonnees_codees = np.array([0, 1, 0, 1, 1, 0])
    print(pop)
    pop.retirer(i2)
    print(pop)