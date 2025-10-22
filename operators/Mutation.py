from core.Individu import individu
import random

class Mutation:
    def __init__(self, taux_mutation: float):
        self.taux_mutation = taux_mutation

    def mutation(self, individu: individu):
        adn = individu.coordonnees.coordonnees_codees
        adn_muté = []

        for bit in adn:
            if random.random() < self.taux_mutation:
                adn_muté.append('1' if bit == '0' else '0')
            else:
                adn_muté.append(bit)

        individu.coordonnees.coordonnees_codees = adn_muté
