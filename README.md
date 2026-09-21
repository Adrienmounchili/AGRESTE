# INF_232_TP — Agreste

Application de collecte et d'analyse statistique des habitudes de programmation des étudiants.
Université de Yaoundé I — TP INF232 EC2.

Version Python (Streamlit), remplace la version initiale en JavaScript.

## Fonctionnalités

- **Tableau de bord** : vue d'ensemble avec KPIs (nombre de réponses, moyenne d'heures, taux d'utilisation de l'IA…)
- **Collecte** : formulaire interactif pour enregistrer les habitudes (âge, année d'étude, langage préféré, heures de code, etc.)
- **Analyse descriptive** : statistiques (moyenne, médiane, écart-type) et graphiques (histogramme, répartition par langage, autonomie par année, satisfaction vs heures)
- **Régression linéaire** : étude de la corrélation entre utilisation de l'IA et autonomie
- **Export CSV** : téléchargement des données collectées

## Technologies

- Python
- Streamlit (interface web)
- Pandas / NumPy (traitement et analyse de données)
- Matplotlib (visualisations)
- SQLite (stockage local des réponses)

## Structure du projet

```
INF_232_TP/
├── app.py            # application Streamlit (interface + navigation)
├── database.py        # connexion SQLite (init, insertion, lecture)
├── analyse.py          # statistiques et régression linéaire
├── requirements.txt
└── .gitignore
```

## Installation

```bash
git clone https://github.com/Adrienmounchili/INF_232_TP.git
cd INF_232_TP
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans le navigateur. Les données sont stockées localement dans `agreste.db` (SQLite), créé automatiquement au premier lancement.

## Auteur

Adrien Mounchili
