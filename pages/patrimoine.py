import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime

from database import SessionLocal
from models.patrimoine import Patrimoine

db = SessionLocal()

st.title("🏠 Gestion du Patrimoine")

# ==================================
# AJOUT D'UN ACTIF / PASSIF
# ==================================

with st.expander("➕ Ajouter un élément"):

    type_bien = st.text_input(
        "Nom"
    )

    categorie = st.selectbox(
        "Catégorie",
        [
            "Compte bancaire",
            "Épargne",
            "Investissement",
            "Immobilier",
            "Véhicule",
            "Autre actif",
            "Dette",
            "Crédit"
        ]
    )

    valeur = st.number_input(
        "Valeur (FCFA)",
        min_value=0.0,
        step=1000.0
    )

    if st.button("Enregistrer"):

        bien = Patrimoine(
            type_bien=type_bien,
            categorie=categorie,
            valeur=valeur,
            date_creation=datetime.now()
        )

        db.add(bien)

        db.commit()

        st.success(
            "Élément enregistré."
        )

        st.rerun()

# ==================================
# LISTE
# ==================================

elements = (
    db.query(Patrimoine)
    .all()
)

data = []

for e in elements:

    data.append(
        {
            "ID": e.id,
            "Bien": e.type_bien,
            "Catégorie": e.categorie,
            "Valeur": e.valeur
        }
    )

df = pd.DataFrame(data)

st.subheader("📋 Patrimoine")

if not df.empty:

    st.dataframe(
        df,
        width="stretch"
    )

# ==================================
# CALCULS
# ==================================

actifs = df[
    ~df["Catégorie"].isin(
        ["Dette", "Crédit"]
    )
]["Valeur"].sum() if not df.empty else 0

passifs = df[
    df["Catégorie"].isin(
        ["Dette", "Crédit"]
    )
]["Valeur"].sum() if not df.empty else 0

patrimoine_net = actifs - passifs

# ==================================
# KPIs
# ==================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Actifs",
        f"{actifs:,.0f} FCFA"
    )

with col2:

    st.metric(
        "Dettes",
        f"{passifs:,.0f} FCFA"
    )

with col3:

    st.metric(
        "Patrimoine Net",
        f"{patrimoine_net:,.0f} FCFA"
    )

# ==================================
# CAMEMBERT
# ==================================

if not df.empty:

    repartition = (
        df.groupby("Catégorie")
        ["Valeur"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        repartition,
        names="Catégorie",
        values="Valeur",
        title="Répartition du patrimoine"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

db.close()
