import sqlite3
import pandas as pd


def create_table_AMA():
    global conn, cursor, df
    conn = sqlite3.connect('database_AMA.db')
    cursor = conn.cursor()

    df = pd.read_excel("./Rifornimenti_Distributori_AMA_2022.xlsx", header=5)
    pd.set_option('display.max_columns', None)

    nominativi()

    mezzi()

    distributori()

    assegnatari()

    sportelli()

    dati_rifornimento()

    cursor.close()
    conn.close()


def nominativi():
    nominativi = df[["Nominativo", "Matricola"]].drop_duplicates()

    cursor.execute('''CREATE TABLE IF NOT EXISTS nominativi(
                    id INTEGER PRIMARY KEY,
                    nominativo TEXT NOT NULL,
                    matricola INT NOT NULL)''')

    for index, row in nominativi.iterrows():
        cursor.execute("INSERT INTO nominativi (nominativo, matricola) VALUES (?, ?)",
                       (row['Nominativo'], row['Matricola']))

    conn.commit()


def distributori():
    distributori = df[["Distributore"]].drop_duplicates()

    cursor.execute('''CREATE TABLE IF NOT EXISTS distributori(
                    id INTEGER PRIMARY KEY,
                    distributore TEXT NOT NULL)''')

    for index, row in distributori.iterrows():
        cursor.execute("INSERT INTO distributori (distributore) VALUES (?)",
                       (row['Distributore'], ))

    conn.commit()


def assegnatari():
    assegnatari = df[["Assegnatario Attuale",
                      "Descrizione Assegnatario"]].drop_duplicates()

    cursor.execute('''CREATE TABLE IF NOT EXISTS assegnatari(
                    id INTEGER PRIMARY KEY,
                    assegnatario_attuale TEXT NOT NULL,
                    descrizione_assegnatario TEXT NOT NULL)''')

    for index, row in assegnatari.iterrows():

        cursor.execute("INSERT INTO assegnatari (assegnatario_attuale, descrizione_assegnatario) VALUES (?, ?)",
                       (row['Assegnatario Attuale'], row['Descrizione Assegnatario']))

    conn.commit()


def sportelli():
    sportelli = df[["Assegnatario Attuale", "Sportello"]].drop_duplicates()

    cursor.execute('''CREATE TABLE IF NOT EXISTS sportelli(
                    id INTEGER PRIMARY KEY,
                    sportello TEXT NOT NULL,
                    assegnatari_id INETGER NOT NULL,
                    FOREIGN KEY (assegnatari_id) REFERENCES assegnatari(id))''')

    for index, row in sportelli.iterrows():
        cursor.execute(
            "SELECT id FROM assegnatari WHERE assegnatario_attuale = ?", (row['Assegnatario Attuale'],))
        assegnatari_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO sportelli (sportello, assegnatari_id) VALUES (?, ?)",
                       (row['Sportello'], assegnatari_id))

    conn.commit()


def mezzi():
    mezzi = df[["Descrizione mezzo"]].drop_duplicates()

    cursor.execute('''CREATE TABLE IF NOT EXISTS mezzi(
                    id INTEGER PRIMARY KEY,
                    descrizione_mezzo TEXT NOT NULL)''')

    for index, row in mezzi.iterrows():
        cursor.execute("INSERT INTO mezzi (descrizione_mezzo) VALUES (?)",
                       (row['Descrizione mezzo'],))

    conn.commit()


def dati_rifornimento():
    cursor.execute('''CREATE TABLE IF NOT EXISTS dati_rifornimento(
                    id INTEGER PRIMARY KEY,
                    data_rifornimento TEXT NOT NULL,
                    ora_rifornimento TEXT NOT NULL,
                    data_registrazione TEXT NOT NULL,
                    ricevuta TEXT NOT NULL,
                    quantita_gasolio NUMERIC NOT NULL,
                    quantita_ADBLUE NUMERIC NOT NULL,
                    strumento TEXT,
                    valore_contattore NUMERIC,
                    differenza_lettura_precedente NUMERIC,
                    note TEXT,
                    mezzo_id INTEGER NOT NULL,
                    sportello_id INTEGER NOT NULL,
                    distributore_id INTEGER NOT NULL,
                    nominativo_id INTEGER NOT NULL,
                    FOREIGN KEY (mezzo_id) REFERENCES mezzi(id),
                    FOREIGN KEY (sportello_id) REFERENCES sportelli(id),
                    FOREIGN KEY (distributore_id) REFERENCES distributori(id),
                    FOREIGN KEY (nominativo_id) REFERENCES nominativi(id)
                    )''')

    for index, row in df.iterrows():
        if (pd.isna(row['Quantità Gasolio'])):
            row['Quantità Gasolio'] = 0

        if (pd.isna(row['Quantità ADBLUE'])):
            row['Quantità ADBLUE'] = 0

        if (pd.isna(row['Strumento'])):
            row['Strumento'] = None

        if (pd.isna(row['Valore CONTAKM/CONTAORE'])):
            row['Valore CONTAKM/CONTAORE'] = None

        if (pd.isna(row['Differenza Lettura Precedente'])):
            row['Differenza Lettura Precedente'] = None

        if (pd.isna(row['Note'])):
            row['Note'] = None

        # Convert the date column to datetime format
        data_rifornimento = row['Data Rifornimento'].strftime('%Y-%m-%d')

        # Convert the date column to datetime format
        data_registrazione = row['Data Registrazione'].strftime('%Y-%m-%d')

        cursor.execute(
            "SELECT id FROM mezzi WHERE descrizione_mezzo = ?", (row['Descrizione mezzo'],))
        mezzo_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT id FROM sportelli WHERE sportello = ?", (row['Sportello'],))
        sportello_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT id FROM distributori WHERE distributore = ?", (row['Distributore'],))
        distributore_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT id FROM nominativi WHERE nominativo = ?", (row['Nominativo'],))
        nominativo_id = cursor.fetchone()[0]

        cursor.execute(
            '''INSERT INTO dati_rifornimento (data_rifornimento, ora_rifornimento, data_registrazione,
            ricevuta, quantita_gasolio, quantita_ADBLUE, strumento, valore_contattore,
            differenza_lettura_precedente, note, mezzo_id, sportello_id, distributore_id, nominativo_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (data_rifornimento, row['Ora Rifornimento'],
             data_registrazione, str(row['Ricevuta/N° Modello']),
             row['Quantità Gasolio'], row['Quantità ADBLUE'],
             row['Strumento'], row['Valore CONTAKM/CONTAORE'],
             row['Differenza Lettura Precedente'], row['Note'],
             mezzo_id, sportello_id, distributore_id, nominativo_id))

    conn.commit()


create_table_AMA()
