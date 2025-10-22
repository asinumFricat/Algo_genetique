from core.Individu import Individu


class Mutation:
    """
    Classe qui permet d'effectuer une mutation sur un individu selon un certain taux de mutation
    """

    def __init__(self, taux_mutation: float):
        self.taux_mutation = taux_mutation

    def mutation(self, individu: Individu):
        """
        Fonction qui prend un individu et effectue des mutations sur ses coordonnées
        """
