from create_tables_AMA import create_table_AMA
from create_tables_stradali import create_table_stradali

import sqlite3


def main():
    create_tables()

    # global conn, cursor, df
    # conn = sqlite3.connect('database_AMA.db')
    # cursor = conn.cursor()

    # average()

    # cursor.close()
    # conn.close()


def create_tables():
    create_table_AMA()
    create_table_stradali()


def average():
    # average quantity of each car type
    cursor.execute('''
        SELECT AVG(dati.quantita_gasolio) AS avg_gasolio, mezzi.descrizione_mezzo FROM dati_rifornimento AS dati
            JOIN mezzi ON
                dati.mezzo_id = mezzi.id WHERE
                    dati.quantita_gasolio > 0
                AND dati.id IN (
                    SELECT 
                )
    ''')


main()
