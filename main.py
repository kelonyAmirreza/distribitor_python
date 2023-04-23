import sqlite3
import pandas as pd


def main():
    global conn, cursor, df
    conn = sqlite3.connect('database_AMA.db')
    cursor = conn.cursor()

    average()

    cursor.close()
    conn.close()


def average():
    # average quantity of each car type
    data = pd.read_sql_query(
        '''
            SELECT dati.quantita_gasolio, dati2.avg_gasolio, mezzi.descrizione_mezzo, nominativi.nominativo 
            FROM dati_rifornimento AS dati
            JOIN mezzi ON dati.mezzo_id = mezzi.id
            JOIN nominativi ON dati.nominativo_id = nominativi.id
            JOIN (
                SELECT AVG(dati2.quantita_gasolio) AS avg_gasolio, dati2.mezzo_id FROM dati_rifornimento AS dati2
                WHERE dati2.quantita_gasolio > 0
                GROUP BY mezzo_id
            ) AS dati2 ON dati.mezzo_id = dati2.mezzo_id
            ORDER BY dati.quantita_gasolio DESC LIMIT 50;
        ''', conn)
    df = pd.DataFrame(data).set_index('nominativo')
    df.to_excel('output_files/output.xlsx')
    print(df)


main()
