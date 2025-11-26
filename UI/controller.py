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

        self._view.lista_visualizzazione.controls.clear()
        self._view.page.update()
        if float(self._view.guadagno_medio_minimo.value) >= 0:

            tratte = self._model.costruisci_grafo(float(self._view.guadagno_medio_minimo.value))
            num_nodi = self._model.get_num_nodes()
            num_tratte_valide = self._model.get_num_edges()


            self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di hub: {num_nodi}"))
            self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di tratte: {num_tratte_valide}"))
            for tratta in tratte:
                self._view.lista_visualizzazione.controls.append(ft.Text(f"{tratta[0]} - {tratta[1]}, guadagno medio tratta: {tratta[2]}"))

            self._view.lista_visualizzazione.update()
            self._view.page.update()
        else:
            self._view.alert.show_alert("Inserisci un valore corretto")
