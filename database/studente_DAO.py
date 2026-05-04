# Add whatever it is needed to interface with the DB Table studente

from database.DB_connect import get_connection
from dataclasses import dataclass

@dataclass
class StudentDAO:
    matricola: int
    cognome: str
    nome: str
    cds: str

    def __hash__(self):
        return hash(self.matricola)

    def __eq__(self, other):
        return self.matricola == other.matricola

    def __str__(self):
        return f"""
        Studente {self.matricola}
        Nome: {self.nome} {self.cognome}
        Corso di studi: {self.cds}
        """