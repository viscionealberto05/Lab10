from networkx.algorithms import threshold

from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.lista_tratte = []
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        self._nodes = DAO.get_hub()
        self.G.add_nodes_from(self._nodes)  #ogni hub diventa un nodo del grafo

        self.lista_tratte = DAO.get_tratte()


    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """

        tratte_universali = []

        for tratta in self.lista_tratte:
            idO = tratta.id_hub_origine
            idD = tratta.id_hub_destinazione
            for nuova_tratta in self.lista_tratte:
                if nuova_tratta.id_hub_destinazione == idO and nuova_tratta.id_hub_origine == idD:
                    tratta.valore_tratta += nuova_tratta.valore_tratta

            tratte_universali.append(tratta)

        for element in tratte_universali:
            print(element)




    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """


    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        # TODO

