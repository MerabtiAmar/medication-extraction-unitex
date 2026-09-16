"""Crée la base SQLite des posologies extraites (exemples issus de la concordance Unitex)."""
import sqlite3

POSOLOGIES = [
    (1, "KARDEGIC", "75mg", "à la demande", "", "", "8 jours"),
    (2, "TAHOR", "80mg", "0,5 cpr", "", "à 8 h", "30 jours"),
    (3, "TRIATEC", "1.25mg", "1 cpr", "", "à 12h", "30 jours"),
    (4, "DAFALGAN", "500mg", "1 cpr", "", "à 18h", "30 jours"),
    (5, "", "", "1 cpr", "", "à 18h", "30 jours"),
    (6, "SIMVASTATINE", "20mg", "1 cpr", "", "à 19h", "18 jours"),
    (7, "SIMVASTATINE", "20mg", "1 cpr", "", "à 19h", "18 jours"),
    (8, "OMEPRAZOLE", "20mg", "1 cpr", "", "à 8h", "30 jours"),
    (9, "SOTALOL", "80mg", "1 cpr", "", "à 8h", "30 jours"),
    (10, "", "", "1 cpr", "", "à 8h", "23 jours"),
    (11, "", "", "1 cpr", "", "à 8h", "23 jours"),
    (12, "LASILIX", "40mg", "2 cpr", "1 cpr à 8h et 1 cpr à 18h", "à 8h et à 18h", "6 jours"),
    (13, "KEPPRA", "250mg", "1 sachet", "", "à 12h", "60 jours"),
    (14, "PLAVIX", "75mg", "2 gel", "", "à 18h", "30 jours"),
    (15, "SINEMET", "100mg", "300mg", "300mg/jour pendant la 2éme semaine", "", ""),
]

connection = sqlite3.connect("extraction.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS EXTRACTION")
cursor.execute("DROP TABLE IF EXISTS POSOLOGIE")
cursor.execute("CREATE TABLE POSOLOGIE(cleP INTEGER PRIMARY KEY, nomP VARCHAR(100), dosageM VARCHAR(20), "
               "dose VARCHAR(100), rythme VARCHAR(100), heure VARCHAR(100), duree VARCHAR(100))")
cursor.executemany("INSERT INTO POSOLOGIE VALUES (?, ?, ?, ?, ?, ?, ?)", POSOLOGIES)
cursor.execute("CREATE TABLE EXTRACTION(id INTEGER PRIMARY KEY, cle INTEGER, FOREIGN KEY (cle) REFERENCES POSOLOGIE(cleP))")
connection.commit()
cursor.close()
connection.close()
print(f"extraction.db créée ({len(POSOLOGIES)} posologies)")

# Merabti Amar
# Meziani Mehdi
