.mod box
SELECT AVG(dati.quantita_gasolio) AS avg_gasolio, mezzi.descrizione_mezzo FROM dati_rifornimento AS dati
JOIN mezzi ON dati.mezzo_id = mezzi.id WHERE dati.quantita_gasolio > 0 GROUP BY mezzi.descrizione_mezzo ORDER BY avg_gasolio DESC;