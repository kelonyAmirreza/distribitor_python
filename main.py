import sqlite3
import pandas as pd


def main():
    global conn_AMA, cursor_AMA, conn_stradali, cursor_stradali
    conn_AMA = sqlite3.connect('database_AMA.db')
    cursor_AMA = conn_AMA.cursor()

    conn_stradali = sqlite3.connect('database_stradali.db')
    cursor_stradali = conn_stradali.cursor()

    average_each_car_perday()
    average_used_each_person()

    cursor_AMA.close()
    conn_AMA.close()
    cursor_stradali.close()
    conn_stradali.close()


def average_each_car_perday():
    # average quantity of each car type per day
    data_AMA = pd.read_sql_query(
        '''
            SELECT AVG(dati.quantita_gasolio) AS avg_gasolio, AVG(dati.quantita_ADBLUE) AS avg_ADBLUE,
                mezzi.descrizione_mezzo FROM dati_rifornimento AS dati
            JOIN mezzi ON dati.mezzo_id = mezzi.id
            GROUP BY dati.mezzo_id
            ORDER BY avg_gasolio DESC, avg_ADBLUE DESC;
        ''', conn_AMA)

    df_AMA = pd.DataFrame(data_AMA).set_index('descrizione_mezzo')

    data_stradali = pd.read_sql_query(
        '''
            SELECT AVG(dati.quantita_gasolio) AS avg_gasolio, AVG(dati.quantita_benzina) AS avg_benzina,
                AVG(dati.quantita_metano) AS avg_metano,  AVG(dati.quantita_GPL) AS avg_GPL, AVG(dati.quantita_ADBLUE) AS avg_ADBLUE,
                mezzi.descrizione_mezzo FROM dati_rifornimento AS dati
            JOIN mezzi ON dati.mezzo_id = mezzi.id
            GROUP BY dati.mezzo_id
            ORDER BY avg_gasolio DESC, avg_benzina DESC, avg_metano DESC, avg_GPL DESC, avg_ADBLUE DESC;
        ''', conn_stradali)

    df_stradali = pd.DataFrame(data_stradali).set_index('descrizione_mezzo')

    with pd.ExcelWriter('output_files/output.xlsx') as writer:
        df_AMA.to_excel(writer, sheet_name='avg_perday_AMA')
        df_stradali.to_excel(
            writer, sheet_name='avg_perday_stradali')


def average_used_each_person():
    # average quantity of each car type per day
    data_AMA = pd.read_sql_query(
        '''
            SELECT AVG(dati.quantita_gasolio) AS avg_gasolio_by_person, 
                AVG(dati.quantita_ADBLUE) AS avg_ADBLUE_by_person,
                dati2.avg_gasolio AS avg_gasolio_by_car, 
                dati2.avg_ADBLUE AS avg_ADBLUE_by_car,
                nominativi.nominativo, 
                mezzi.descrizione_mezzo
            FROM dati_rifornimento AS dati
            JOIN nominativi ON nominativi.id = dati.nominativo_id
            JOIN mezzi ON dati.mezzo_id = mezzi.id
            JOIN (
                SELECT dati3.mezzo_id,
                    AVG(dati3.quantita_gasolio) AS avg_gasolio, 
                    AVG(dati3.quantita_ADBLUE) AS avg_ADBLUE
                FROM dati_rifornimento AS dati3
                GROUP BY dati3.mezzo_id
            ) AS dati2 ON dati2.mezzo_id = mezzi.id
            GROUP BY dati.nominativo_id
            ORDER BY avg_gasolio_by_person DESC, avg_gasolio_by_car limit 50;
        ''', conn_AMA)

    df_AMA = pd.DataFrame(data_AMA).set_index('nominativo')

    data_stradali = pd.read_sql_query(
        '''
            SELECT AVG(dati.quantita_gasolio) AS avg_gasolio_by_person,
                AVG(dati.quantita_benzina) AS avg_benzina_by_person,
                AVG(dati.quantita_metano) AS avg_metano_by_person,
                AVG(dati.quantita_GPL) AS avg_GPL_by_person,
                AVG(dati.quantita_ADBLUE) AS avg_ADBLUE_by_person,
                dati2.avg_gasolio AS avg_gasolio_by_car, 
                dati2.avg_benzina AS avg_benzina_by_car,
                dati2.avg_metano AS avg_metano_by_car,
                dati2.avg_GPL AS avg_GPL_by_car,
                dati2.avg_ADBLUE AS avg_ADBLUE_by_car,
                nominativi.nominativo, 
                mezzi.descrizione_mezzo
            FROM dati_rifornimento AS dati
            JOIN nominativi ON nominativi.id = dati.nominativo_id
            JOIN mezzi ON dati.mezzo_id = mezzi.id
            JOIN (
                SELECT dati3.mezzo_id,
                    AVG(dati3.quantita_gasolio) AS avg_gasolio,
                    AVG(dati3.quantita_benzina) AS avg_benzina,
                    AVG(dati3.quantita_metano) AS avg_metano,
                    AVG(dati3.quantita_GPL) AS avg_GPL,
                    AVG(dati3.quantita_ADBLUE) AS avg_ADBLUE
                FROM dati_rifornimento AS dati3
                GROUP BY dati3.mezzo_id
            ) AS dati2 ON dati2.mezzo_id = mezzi.id
            GROUP BY dati.nominativo_id
            ORDER BY avg_gasolio_by_person DESC, avg_gasolio_by_car limit 50;
        ''', conn_stradali)

    df_stradali = pd.DataFrame(data_stradali).set_index('nominativo')

    with pd.ExcelWriter('output_files/output1.xlsx') as writer:
        df_AMA.to_excel(writer, sheet_name='avg_perday_AMA')
        df_stradali.to_excel(
            writer, sheet_name='avg_perday_stradali')


main()
