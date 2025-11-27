import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """

        #Pulisco la listview per non avere i risultati della ricerca precedente

        self._view.lista_visualizzazione.controls.clear()
        self._view.page.update()

        #Verifico le condizioni di controllo

        try:
            if float(self._view.guadagno_medio_minimo.value) >= 0:

                #Ottengo tutti i valori che devo passare alla View dal Model

                grafo = self._model.costruisci_grafo(float(self._view.guadagno_medio_minimo.value))
                num_nodi = self._model.get_num_nodes()
                num_tratte_valide = self._model.get_num_edges()
                tratte = []

                """Per mostrare dei risultati interpretabili nella view, associo gli id degli hub che si trovano
                negli archi (tuple con 3 valori) agli id degli hub presenti come nodi, così da risalire ai nomi
                degli hub di partenza e di arrivo; successivamente passo i valori alla ListView contenuta nella View"""

                for arco in grafo.edges(data=True):

                    #Scelgo di gestire la singola tratta come dizionario, e costruire una lista di dizionari
                    #per facilitarmi la sintassi nella stampa

                    tratta = {}
                    nome_origine = None
                    nome_destinazione = None

                    # Trovo nome hub origine
                    for hub in grafo.nodes:
                        if hub.id == arco[0]:
                            nome_origine = hub.nome
                            break

                    # Trovo nome hub destinazione
                    for hub in grafo.nodes:
                        if hub.id == arco[1]:
                            nome_destinazione = hub.nome
                            break

                    # Aggiungo alla lista il dizionario

                    tratta["hub_origine"] = nome_origine
                    tratta["hub_destinazione"] = nome_destinazione
                    tratta["valore_tratta"] = arco[2]["weight"]
                    tratte.append(tratta)

                self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di hub: {num_nodi}"))
                self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di tratte: {num_tratte_valide}"))
                for tratta in tratte:
                    self._view.lista_visualizzazione.controls.append(ft.Text(f"{tratta['hub_origine']} ---> {tratta['hub_destinazione']}, guadagno medio tratta: {tratta['valore_tratta']}"))

                self._view.lista_visualizzazione.update()
                self._view.page.update()

            else:
                self._view.alert.show_alert("Inserisci un valore positivo.")

        except ValueError:
            self._view.alert.show_alert("Inserisci un valore corretto.")
