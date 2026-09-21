# Adrien Mounchili

import sqlite3
import pandas as pd

DB_PATH = "agreste.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reponses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            annee_etude TEXT,
            heures_code REAL,
            langage TEXT,
            utilise_ia INTEGER,
            autonomie INTEGER,
            satisfaction INTEGER,
            projets INTEGER,
            date_creation TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def ajouter_reponse(reponse: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO reponses
           (age, annee_etude, heures_code, langage, utilise_ia, autonomie, satisfaction, projets)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            reponse["age"],
            reponse["annee_etude"],
            reponse["heures_code"],
            reponse["langage"],
            int(reponse["utilise_ia"]),
            reponse["autonomie"],
            reponse["satisfaction"],
            reponse["projets"],
        ),
    )
    conn.commit()
    conn.close()


def charger_donnees() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM reponses ORDER BY date_creation DESC", conn)
    conn.close()
    if not df.empty:
        df["utilise_ia"] = df["utilise_ia"].astype(bool)
    return df
