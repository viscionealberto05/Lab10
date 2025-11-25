from database.DB_connect import DBConnect
from model.hub import Hub
from model.tratta import Tratta

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def get_hub():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Mancata connessione al DB")

        else:
            cursor = cnx.cursor(dictionary=True)
            query = ("SELECT * FROM hub")
            cursor.execute(query)

            for row in cursor:
                result.append(Hub(row["id"],
                                  row["nome"],
                                  row["codice"],
                                  row["citta"],
                                  row["stato"],
                                  row["latitudine"],
                                  row["longitudine"]))

            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def get_tratte():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Mancata connessione al DB")

        else:
            cursor = cnx.cursor(dictionary=True)

            query = ("""SELECT id_hub_origine, id_hub_destinazione, AVG(valore_merce) as media
                     FROM spedizione
                     GROUP BY id_hub_origine, id_hub_destinazione""")

            cursor.execute(query)

            for row in cursor:
                result.append(Tratta(row["id_hub_origine"],row["id_hub_destinazione"],row["media"]))

            cursor.close()
        cnx.close()
        return result

