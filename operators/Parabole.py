from dataclasses import dataclass
from typing import Sequence


@dataclass
class Parabole:
    """
    Fonction de test utilisée dans les algorithmes génétiques.
    Définition : f(x) = ∑ x_i²
    (minimum global en x = 0)
    """
    dimension: int | None = None
    bornes: tuple[float, float] = (-100.0, 100.0)

    def __call__(self, vecteur: Sequence[float]) -> float:
        """Calcule la somme des carrés des composantes du vecteur."""
        if self.dimension is not None and len(vecteur) != self.dimension:
            raise ValueError(f"Dimension attendue = {self.dimension}, reçue = {len(vecteur)}.")
        return sum(x * x for x in vecteur)

    def evaluer(self, vecteur: Sequence[float]) -> float:
        """Alias plus explicite pour évaluer la fonction."""
        return self(vecteur)
