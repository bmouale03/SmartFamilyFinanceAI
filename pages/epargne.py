import streamlit as st
import pandas as pd

from database import SessionLocal
from models.epargne import Epargne
from models.compte import Compte

st.set_page_config(
    page_title="Gestion de l'Épargne",
    page_icon="🏦",
    layout="wide"
)

st.title("Gestion de l'Épargne")

db = SessionLocal()

# =====================================
# Chargement des données
# =====================================

epargnes = db.query(Epargne).all()

data = []

for e in epargnes:

    compte = (
        db.query(Compte)
        .filter(
            Compte.id == e.compte_id
        )
        .first()
    )

    data.append(
        {
            "ID": e.id,
            "Mois Budget": e.mois_budget,
            "Date": e.date_operation,
            "Compte": (
                compte.nom_compte
                if compte
                else ""
            ),
            "Montant": float(e.montant),
            "Observation": e.observation
        }
    )

df = pd.DataFrame(data)

# =====================================
# KPI
# =====================================

total_epargne = (
    df["Montant"].sum()
    if not df.empty
    else 0
)

st.metric(
    "💰 Épargne Totale",
    f"{total_epargne:,.0f} FCFA"
)

# =====================================
# Tableau
# =====================================

st.subheader(
    "Liste des Épargnes"
)

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

st.markdown("---")

# =====================================
# Ajout
# =====================================

st.subheader(
    "➕ Ajouter une Épargne"
)

comptes = db.query(Compte).all()

if comptes:

    comptes_dict = {
        c.nom_compte: c.id
        for c in comptes
    }

    with st.form("ajout_epargne"):

        mois_budget = st.text_input(
            "Mois Budget",
            placeholder="Ex : Janvier 2026"
        )

        date_operation = st.date_input(
            "Date de l'opération"
        )

        nom_compte = st.selectbox(
            "Compte",
            list(comptes_dict.keys())
        )

        montant = st.number_input(
            "Montant",
            min_value=0.0,
            step=1000.0
        )

        observation = st.text_input(
            "Observation"
        )

        submit = st.form_submit_button(
            "Ajouter"
        )

        if submit:

            epargne = Epargne(
                mois_budget=mois_budget,
                compte_id=comptes_dict[nom_compte],
                date_operation=date_operation,
                montant=montant,
                observation=observation
            )

            db.add(epargne)

            db.commit()

            st.success(
                "Épargne ajoutée avec succès."
            )

            st.rerun()

else:

    st.warning(
        "Aucun compte disponible. Veuillez créer un compte dans le menu Comptes."
    )

# =====================================
# Modification
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "✏️ Modifier une Épargne"
    )

    epargne_id = st.selectbox(
        "Choisir une opération",
        df["ID"]
    )

    epargne = (
        db.query(Epargne)
        .filter(
            Epargne.id == epargne_id
        )
        .first()
    )

    nouveau_mois = st.text_input(
        "Mois Budget",
        value=epargne.mois_budget or ""
    )

    nouvelle_date = st.date_input(
        "Date",
        value=epargne.date_operation
    )

    nouveau_montant = st.number_input(
        "Montant",
        value=float(epargne.montant)
    )

    nouvelle_observation = st.text_input(
        "Observation",
        value=epargne.observation or ""
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Mettre à jour"
        ):

            epargne.mois_budget = nouveau_mois

            epargne.date_operation = (
                nouvelle_date
            )

            epargne.montant = (
                nouveau_montant
            )

            epargne.observation = (
                nouvelle_observation
            )

            db.commit()

            st.success(
                "Épargne mise à jour."
            )

            st.rerun()

    with col2:

        if st.button(
            "🗑️ Supprimer"
        ):

            db.delete(
                epargne
            )

            db.commit()

            st.success(
                "Épargne supprimée."
            )

            st.rerun()

# =====================================
# Analyse
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "Répartition de l'Épargne par Compte"
    )

    repartition = (
        df.groupby("Compte")["Montant"]
        .sum()
        .reset_index()
    )

    st.bar_chart(
        repartition.set_index(
            "Compte"
        )
    )

# =====================================
# Analyse par Mois
# =====================================

if (
    not df.empty
    and "Mois Budget" in df.columns
):

    st.markdown("---")

    st.subheader(
        "📅 Épargne par Mois Budgétaire"
    )

    repartition_mois = (
        df.groupby("Mois Budget")["Montant"]
        .sum()
        .reset_index()
    )

    st.bar_chart(
        repartition_mois.set_index(
            "Mois Budget"
        )
    )