from dataclasses import dataclass, field
from typing import Iterable
import statistics as stats
import csv
from pathlib import Path


@dataclass
class Performance:
    """
    Classe qui enregistre les performances d’un algorithme génétique
    au fil des générations.
    """
    generations: list[int] = field(default_factory=list)
    meilleurs: list[float] = field(default_factory=list)
    medianes: list[float] = field(default_factory=list)
    moyennes: list[float] = field(default_factory=list)
    pires: list[float] = field(default_factory=list)
    ecarts_type: list[float] = field(default_factory=list)

    def enregistrer(self, generation: int, valeurs_fitness: Iterable[float]) -> None:
        """Enregistre les statistiques d’une génération donnée."""
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
        """Exporte les performances enregistrées dans un fichier CSV."""
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
