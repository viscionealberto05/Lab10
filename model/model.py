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

        self.G.clear() #PULISCO IL GRAFICO, ALTRIMENTI POTENZIALI RICHIESTE SUCCESSIVE SI AGGIUNGONO E NON SOVRASCRIVONO I DATI

        self._nodes = DAO.get_hub() #recupero i nodi come oggetti di tipo hub dal DAO
        self.G.add_nodes_from(self._nodes)

        self.lista_tratte = DAO.get_tratte() #recupero la lista completa delle tratte dal DAO, query semplice
        self._edges = []

        for tratta in self.get_all_edges():

            #Verifico che il valore della tratta per la merce sia superiore a quello ricevuto dal controller
            #aggiungo dunque l'arco al grafo

            if tratta.valore_tratta >= threshold:

                # Aggiungo edge al grafo
                self.G.add_edge(
                    tratta.id_hub_origine,
                    tratta.id_hub_destinazione,
                    weight=tratta.valore_tratta
                )

                """
                POTENZIALE SOLUZIONE ALTERNATIVA ANALIZZANDO LE TRATTE
                VALIDE DIRETTAMENTE NEL MODEL, RESTITUENDO AL CONTROLLER
                LE SOLE TRATTE DA STAMPARE (SOTTO FORMA DI LISTA DI LISTE
                O COME LISTA DI DIZIONARI)
                
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

                # Creo la lista
                result = [nome_origine, nome_destinazione, tratta.valore_tratta]

                # La aggiungo alla lista di edge
                self._edges.append(result)"""

        return self.G


    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        return len(self.G.edges())


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

        """Approccio con query SQL semplice:
        
        Ho recuperato dal DAO tutte le tratte, e alcune risultano duplicate (A->B;B->A)
        dunque creo una nuova lista che non conterrà duplicati, aggiungo gradualmente le singole
        tratte, chiedendomi se si trovano già all'interno, mediante una verifica su id di partenza
        e di destinazione. Se dovessi trovare che una tratta analoga è gia presente, modifico la media 
        di quella che si trovava già nella lista unificata."""

        tratte_unificate = []

        for tratta in self.lista_tratte:

            idO = tratta.id_hub_origine
            idD = tratta.id_hub_destinazione
            trovata = False

            for tratta_nuova in tratte_unificate:

                if tratta_nuova.id_hub_origine == idD and tratta_nuova.id_hub_destinazione == idO:

                    tratta_nuova.valore_tratta += tratta.valore_tratta
                    tratta_nuova.valore_tratta = round(tratta_nuova.valore_tratta/2,3)
                    trovata = True
                    break

            if not trovata:
                tratte_unificate.append(tratta)

        return tratte_unificate

