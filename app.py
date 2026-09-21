# Adrien Mounchili

import streamlit as st
import matplotlib.pyplot as plt

from database import init_db, ajouter_reponse, charger_donnees
from analyse import moyenne, mediane, ecart_type, regression_lineaire, interpreter_r2

st.set_page_config(page_title="Agreste — Habitudes des codeurs", page_icon="📊", layout="wide")

init_db()

ANNEES = ["L1", "L2", "L3", "M1", "M2"]
LANGAGES = ["JavaScript", "Python", "Java", "C++", "Autre"]

st.title("📊 Agreste — Enquête sur les habitudes des codeurs")
st.caption("TP INF232 EC2 — Université de Yaoundé I")

onglet = st.sidebar.radio(
    "Navigation",
    ["Tableau de bord", "Collecte", "Analyse", "Régression", "Export CSV"],
)

df = charger_donnees()


# ---------- TABLEAU DE BORD ----------
if onglet == "Tableau de bord":
    st.header("Tableau de bord")

    if df.empty:
        st.info("Aucune donnée collectée pour le moment. Rendez-vous dans l'onglet **Collecte** pour commencer.")
    else:
        pct_ia = (df["utilise_ia"].sum() / len(df)) * 100

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Réponses totales", len(df))
        c2.metric("Moy. heures/semaine", f"{moyenne(df['heures_code']):.2f}")
        c3.metric("Moy. autonomie", f"{moyenne(df['autonomie']):.2f}/10")
        c4.metric("Moy. satisfaction", f"{moyenne(df['satisfaction']):.2f}/10")
        c5.metric("Utilisent l'IA", f"{pct_ia:.1f}%")

        st.subheader("Répartition par année d'étude")
        repartition = df["annee_etude"].value_counts().reindex(ANNEES, fill_value=0)

        fig, ax = plt.subplots()
        ax.bar(repartition.index, repartition.values, color="#10b981")
        ax.set_ylabel("Nombre de réponses")
        st.pyplot(fig)


# ---------- COLLECTE ----------
elif onglet == "Collecte":
    st.header("Collecte de données")
    st.write("Remplissez le formulaire ci-dessous pour enregistrer vos habitudes de programmation.")

    with st.form("formulaire_reponse", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Âge", min_value=16, max_value=70, value=21)
            annee_etude = st.selectbox("Année d'étude", ANNEES)
            heures_code = st.number_input("Heures de code / semaine", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
            langage = st.selectbox("Langage préféré", LANGAGES)

        with col2:
            utilise_ia = st.radio("Utilisez-vous l'IA pour coder ?", ["Oui", "Non"], horizontal=True)
            autonomie = st.slider("Autonomie", 1, 10, 5)
            satisfaction = st.slider("Satisfaction", 1, 10, 5)
            projets = st.number_input("Projets personnels réalisés", min_value=0, max_value=999, value=0)

        envoyer = st.form_submit_button("Envoyer")

        if envoyer:
            ajouter_reponse({
                "age": age,
                "annee_etude": annee_etude,
                "heures_code": heures_code,
                "langage": langage,
                "utilise_ia": utilise_ia == "Oui",
                "autonomie": autonomie,
                "satisfaction": satisfaction,
                "projets": projets,
            })
            st.success("Réponse enregistrée avec succès ! Vous pouvez en ajouter une autre.")


# ---------- ANALYSE ----------
elif onglet == "Analyse":
    st.header("Analyse descriptive")

    if df.empty:
        st.info("Aucune donnée à analyser.")
    else:
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Âge moyen", f"{moyenne(df['age']):.2f}")
        c2.metric("Âge médian", f"{mediane(df['age']):.2f}")
        c3.metric("Écart-type âge", f"{ecart_type(df['age']):.2f}")
        c4.metric("Moy. heures/sem", f"{moyenne(df['heures_code']):.2f}")
        c5.metric("Médiane heures", f"{mediane(df['heures_code']):.2f}")
        c6.metric("Moy. projets", f"{moyenne(df['projets']):.2f}")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Histogramme des âges")
            fig, ax = plt.subplots()
            ax.hist(df["age"], bins=range(int(df["age"].min()), int(df["age"].max()) + 5, 5), color="#10b981", edgecolor="white")
            ax.set_xlabel("Âge")
            ax.set_ylabel("Nombre")
            st.pyplot(fig)

        with col2:
            st.subheader("Langages préférés")
            repartition_lang = df["langage"].value_counts()
            fig, ax = plt.subplots()
            ax.pie(repartition_lang.values, labels=repartition_lang.index, autopct="%1.0f%%")
            st.pyplot(fig)

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Autonomie moyenne par année")
            auto_par_annee = df.groupby("annee_etude")["autonomie"].mean().reindex(ANNEES)
            fig, ax = plt.subplots()
            ax.bar(auto_par_annee.index, auto_par_annee.values, color="#3b82f6")
            ax.set_ylabel("Autonomie moyenne")
            st.pyplot(fig)

        with col4:
            st.subheader("Satisfaction vs Heures de code")
            fig, ax = plt.subplots()
            ax.scatter(df["heures_code"], df["satisfaction"], color="#f59e0b")
            ax.set_xlabel("Heures/semaine")
            ax.set_ylabel("Satisfaction")
            st.pyplot(fig)

        st.subheader("Dernières réponses")
        st.dataframe(df.drop(columns=["id"]), use_container_width=True)


# ---------- REGRESSION ----------
elif onglet == "Régression":
    st.header("Régression linéaire")
    st.write("Étude de la relation entre l'utilisation de l'IA et le niveau d'autonomie.")

    if len(df) < 2:
        st.info("Au moins 2 réponses sont nécessaires pour la régression.")
    else:
        x = df["utilise_ia"].astype(int)
        y = df["autonomie"]

        resultat = regression_lineaire(x, y)

        st.latex(f"y = {resultat['a']:.2f}x + {resultat['b']:.2f}")

        c1, c2, c3 = st.columns(3)
        c1.metric("R²", f"{resultat['r2']:.2f}")
        c2.metric("Pente (a)", f"{resultat['a']:.2f}")
        c3.metric("Observations", resultat["n"])

        st.info(interpreter_r2(resultat["r2"]))

        st.subheader("Nuage de points avec droite de régression")
        fig, ax = plt.subplots()
        ax.scatter(x, y, color="#10b981", s=80, label="Données")
        x_ligne = [0, 1]
        y_ligne = [resultat["b"], resultat["a"] + resultat["b"]]
        ax.plot(x_ligne, y_ligne, color="#f59e0b", linewidth=2, label="Droite de régression")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Non", "Oui"])
        ax.set_xlabel("Utilise l'IA")
        ax.set_ylabel("Autonomie")
        ax.legend()
        st.pyplot(fig)


# ---------- EXPORT CSV ----------
elif onglet == "Export CSV":
    st.header("Export CSV")
    st.write("Téléchargez l'ensemble des données collectées.")

    st.metric("Enregistrements disponibles", len(df))

    if df.empty:
        st.info("Aucune donnée à exporter.")
    else:
        csv = df.drop(columns=["id"]).to_csv(index=False).encode("utf-8")
        st.download_button("Exporter en CSV", data=csv, file_name="agreste_donnees.csv", mime="text/csv")

        st.subheader("Aperçu (5 dernières réponses)")
        st.dataframe(df.drop(columns=["id"]).head(5), use_container_width=True)
