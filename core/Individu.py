import numpy as np
from core.Individu import individu
from core.Coordonnees import coordonnees
from operators.Codage import Codage


class population:
    def __init__(self, liste_individus: list[individu] = None):
        self.liste_individus = liste_individus if liste_individus else []
class individu:
    def __init__(self, id: int, coordonnees: coordonnees, codage: Codage = None):
        self.id = id  # Identifiant unique
        self.coordonnees = coordonnees
        self.elite = False  # Pour d'éventuelles stratégies d'élitisme
        self.fitness = None  # Calculée selon la fonction de performance (benchmark)
        
        if codage:
            # Codage automatique dès l'initialisation
            codage.code(self.coordonnees)

    def __str__(self):
        if len(self.liste_individus) == 0:
            return "La population est vide."
        else:
            x = ",\n".join(str(ind) for ind in self.liste_individus)
            return f"La population est composée des individus suivants : \n{x}"

    def ajouter(self, individus: individu | list[individu]):
        if isinstance(individus, list):
            self.liste_individus.extend(individus)
        else:
            self.liste_individus.append(individus)

    def retirer(self, individus: individu | list[individu]):
        if isinstance(individus, list):
            self.liste_individus = [x for x in self.liste_individus if x not in individus]
        else:
            self.liste_individus.remove(individus)

    def generer_population_aleatoire(
        self,
        taille_population: int,
        dimensions: int,
        fenetre_recherche: list[tuple[float, float]],
        codage: Codage,
    ):
        """
        Génère une population aléatoire en respectant la fenêtre de recherche pour chaque coordonnée,
        puis encode chaque individu avec la méthode de codage passée.
        
        Args:
            taille_population (int): nombre d'individus à générer
            dimensions (int): nombre de coordonnées par individu
            fenetre_recherche (list of tuples): liste des (min, max) pour chaque dimension
            codage (Codage): objet de codage à appliquer sur chaque individu
        """
        self.liste_individus.clear()
        for i in range(taille_population):
            coords = np.array(
                [
                    np.random.uniform(fenetre_recherche[dim][0], fenetre_recherche[dim][1])
                    for dim in range(dimensions)
                ]
            )
            coord_obj = coordonnees(coords)
            ind = individu(id=i + 1, coordonnees=coord_obj, codage=codage)
            self.ajouter(ind)
        return (f"ID : {self.id}, "
                f"coordonnées : {self.coordonnees.coordonnees}, "
                f"codées : {self.coordonnees.coordonnees_codees}, "
                f"fitness : {self.fitness}, elite : {self.elite}")

# === Test ===
if __name__ == "__main__":
    import numpy as np
    from core.Coordonnees import coordonnees
    from operators.Codage import CodageMantisseExposant

    taille_pop = 50
    dims = 3
    fenetre = [(-10, 10)] * dims  # Fenêtre de recherche [-10, 10] pour chaque coordonnée
    # Create raw coordinates
    coords = coordonnees(np.array([1.5, -3.2]))

    # Create coder
    coder = CodageMantisseExposant(bits_per_var=16, exponent_bits=5)

    pop = population()
    pop.generer_population_aleatoire(taille_pop, dims, fenetre, coder)
    print(pop)
    # Create individual with automatic codage
    ind = individu(1, coords, codage=coder)
    print(ind)
