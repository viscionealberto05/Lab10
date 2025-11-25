#tratta -> edge
from dataclasses import dataclass

@dataclass
class Tratta():
    id_hub_origine : int
    id_hub_destinazione : int
    valore_tratta : float


    def __str__(self):
        return f"Hub: ({self.id_hub_origine},{self.id_hub_destinazione}) con valore tratta {self.valore_tratta}"

