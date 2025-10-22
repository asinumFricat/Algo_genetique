from abc import ABC, abstractmethod
from core.Coordonnees import coordonnees
import numpy as np


class Codage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def codage(self, coord: coordonnees):
        """
        Fonction qui prend les coordonnées réelles et les encode
        """
        pass


class codage_binaire(Codage):
    def __init__(self, taille_mantisse=10, taille_exposant=6):
        self.taille_mantisse = taille_mantisse
        self.taille_exposant = taille_exposant
        self.total_bits = taille_mantisse + taille_exposant

    def codage(self, variables, bornes=None):
        """
        variables: list or np.array of floats
        bornes: list of tuples [(min1, max1), (min2, max2), ...]
        returns list of bits encoding variables with mantissa-exponent binary representation
        """
        if bornes is None:
            bornes = [(-100, 100)] * len(variables)  # default bounds

        encoded = []
        for i, val in enumerate(variables):
            min_val, max_val = bornes[i]

            # Normalize val in [min_val, max_val] to [0,1]
            norm = (val - min_val) / (max_val - min_val)

            # Map norm to an integer in the range of 2^(total_bits)-1
            max_int = 2 ** self.total_bits - 1
            int_val = int(norm * max_int)

            # Convert int_val to binary string with leading zeros
            bin_str = format(int_val, f'0{self.total_bits}b')

            # Append bits as integers to encoded list
            encoded.extend([int(b) for b in bin_str])

        return np.array(encoded)


class codage_reel(Codage):
    def codage(self, variables):
        """
        Transforme chaque élément de la liste en float (pas vraiment un codage)
        """
        return [float(v) for v in variables]


if __name__ == "__main__":
    x = [1, 2.5, 3, 4.7]
    codagereel = codage_reel()
    codagebinaire = codage_binaire()
    print("Codage réel:", codagereel.codage(x))
    print("Codage binaire:", codagebinaire.codage(x))
