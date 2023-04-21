.mod box
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