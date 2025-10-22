from dataclasses import dataclass, field
from typing import Iterable, Sequence
import statistics as stats
import csv
from pathlib import Path


# ============================================================
# Classe Parabole
# ============================================================

@dataclass
class Parabole:
    """
    Fonction de test utilisée dans les algorithmes génétiques.
    Définition : f(x) = ∑ x_i²
    (minimum global en x = 0)

    Exemple :
        f = Parabole()
        valeur = f([1.0, 2.0, -3.0])  # renvoie 14.0
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


# ============================================================
# Classe Performance
# ============================================================

@dataclass
class Performance:
    """
    Classe qui enregistre les performances d’un algorithme génétique
    au fil des générations.

    Exemple d’utilisation :
        perf = Performance()
        perf.enregistrer(0, [1.2, 0.8, 2.5])
        perf.enregistrer(1, [0.9, 0.5, 1.3])
        perf.exporter_csv("resultats.csv")
    """
    generations: list[int] = field(default_factory=list)
    meilleurs: list[float] = field(default_factory=list)
    medianes: list[float] = field(default_factory=list)
    moyennes: list[float] = field(default_factory=list)
    pires: list[float] = field(default_factory=list)
    ecarts_type: list[float] = field(default_factory=list)

    def enregistrer(self, generation: int, valeurs_fitness: Iterable[float]) -> None:
        """
        Enregistre les statistiques d’une génération donnée.

        :param generation: numéro de la génération
        :param valeurs_fitness: liste ou itérable de valeurs de fitness
        """
        valeurs = list(valeurs_fitness)
        if not valeurs:
            raise ValueError("Aucune valeur de fitness fournie.")

        self.generations.append(generation)
        self.meilleurs.append(min(valeurs))
        self.medianes.append(stats.median(valeurs))
        self.moyennes.append(stats.fmean(valeurs))
        self.pires.append(max(valeurs))
        self.ecarts_type.append(stats.pstdev(valeurs))

    def exporter_csv(self, chemin: str | Path) -> None:
        """
        Exporte les performances enregistrées dans un fichier CSV.

        Colonnes : génération, meilleur, médiane, moyenne, pire, écart_type
        """
        chemin = Path(chemin)
        chemin.parent.mkdir(parents=True, exist_ok=True)

        with chemin.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["generation", "meilleur", "mediane", "moyenne", "pire", "ecart_type"])
            for i in range(len(self.generations)):
                writer.writerow([
                    self.generations[i],
                    self.meilleurs[i],
                    self.medianes[i],
                    self.moyennes[i],
                    self.pires[i],
                    self.ecarts_type[i],
                ])
