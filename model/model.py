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
        """self._nodes = DAO.get_hub()
        self.G.add_nodes_from(self._nodes)  #ogni hub diventa un nodo del grafo

        self.lista_tratte = DAO.get_tratte()
        self._edges = []
        result=[]

        for tratta in self.get_all_edges():
            result = []
            if tratta.valore_tratta >= float(threshold):
                self.G.add_edge(tratta.id_hub_origine, tratta.id_hub_destinazione, weight=tratta.valore_tratta)
                for hub_origine in self._nodes:
                    if hub_origine.id == tratta.id_hub_origine:
                        result.append(hub_origine.nome)
                        for hub_destinazione in self._nodes:
                            if hub_destinazione.id == tratta.id_hub_destinazione:
                                result.append(hub_destinazione.nome)
                                result.append(tratta.valore_tratta)
                                break
                    break

        self._edges.append(result)

        return self._edges"""

        self._nodes = DAO.get_hub()
        self.G.add_nodes_from(self._nodes)

        self.lista_tratte = DAO.get_tratte()
        self._edges = []

        for tratta in self.get_all_edges():

            if tratta.valore_tratta >= float(threshold):

                # Aggiungo edge al grafo
                self.G.add_edge(
                    tratta.id_hub_origine,
                    tratta.id_hub_destinazione,
                    weight=tratta.valore_tratta
                )

                nome_origine = None
                nome_destinazione = None

                # Trovo nome hub origine
                for hub in self._nodes:
                    if hub.id == tratta.id_hub_origine:
                        nome_origine = hub.nome
                        break

                # Trovo nome hub destinazione
                for hub in self._nodes:
                    if hub.id == tratta.id_hub_destinazione:
                        nome_destinazione = hub.nome
                        break

                # Creo la lista nel formato che vuoi tu
                result = [nome_origine, nome_destinazione, tratta.valore_tratta]

                # La aggiungo alla lista di edge
                self._edges.append(result)

        return self._edges



    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        return len(self._edges)





    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """

        return len(self._nodes)


    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """

        tratte_unificate = []

        for tratta in self.lista_tratte:

            """idO = tratta.id_hub_origine
            idD = tratta.id_hub_destinazione
            check = False

            if len(tratte_unificate) != 0:
                for tratta_unificata in tratte_unificate:
                    if (tratta_unificata.id_hub_destinazione == idO and tratta_unificata.id_hub_origine == idD or
                            tratta_unificata.id_hub_destinazione == idD and tratta_unificata.id_hub_origine == idO):
                        tratta_unificata.valore_tratta += tratta.valore_tratta
                        check = True
                if tratta not in tratte_unificate and check == False:
                    tratte_unificate.append(tratta)
            else:
                tratte_unificate.append(tratta)

        return tratte_unificate"""

        for tratta in self.lista_tratte:
            idO = tratta.id_hub_origine
            idD = tratta.id_hub_destinazione

            trovata = False

            for tratta_nuova in tratte_unificate:
                if ((tratta_nuova.id_hub_origine == idO and tratta_nuova.id_hub_destinazione == idD) or
                        (tratta_nuova.id_hub_origine == idD and tratta_nuova.id_hub_destinazione == idO)):
                    tratta_nuova.valore_tratta += tratta.valore_tratta
                    tratta_nuova.valore_tratta = tratta_nuova.valore_tratta/2
                    trovata = True
                    break

            if not trovata:
                tratte_unificate.append(tratta)


        return tratte_unificate

