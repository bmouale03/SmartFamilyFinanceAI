import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import func

from database import SessionLocal

from models.revenu import Revenu
from models.depense import Depense
from models.epargne import Epargne
from models.objectif import Objectif


st.set_page_config(
    page_title="Rapports",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Rapports Financiers")

db = SessionLocal()

# =====================================================
# INDICATEURS GLOBAUX
# =====================================================

total_revenus = (
    db.query(
        func.sum(Revenu.montant)
    ).scalar()
    or 0
)

total_depenses = (
    db.query(
        func.sum(Depense.montant)
    ).scalar()
    or 0
)

total_epargne = (
    db.query(
        func.sum(Epargne.montant)
    ).scalar()
    or 0
)

solde_net = (
    float(total_revenus)
    - float(total_depenses)
    - float(total_epargne)
)

st.subheader("Résumé Financier")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Revenus",
    f"{float(total_revenus):,.0f} FCFA"
)

c2.metric(
    "💸 Dépenses",
    f"{float(total_depenses):,.0f} FCFA"
)

c3.metric(
    "🏦 Épargne",
    f"{float(total_epargne):,.0f} FCFA"
)

c4.metric(
    "📈 Solde Net",
    f"{solde_net:,.0f} FCFA"
)

st.divider()

# =====================================================
# TAUX D'EPARGNE
# =====================================================

st.subheader("Taux d'Épargne")

if float(total_revenus) > 0:

    taux_epargne = (
        float(total_epargne)
        / float(total_revenus)
    ) * 100

    st.metric(
        "Taux d'Épargne",
        f"{taux_epargne:.2f}%"
    )

else:

    st.warning(
        "Aucun revenu disponible."
    )

st.divider()

# =====================================================
# REPARTITION DES DEPENSES
# =====================================================

st.subheader("Répartition des Dépenses")

depenses = db.query(
    Depense
).all()

if depenses:

    data_depenses = []

    for d in depenses:

        data_depenses.append(
            {
                "Catégorie": d.categorie,
                "Montant": float(d.montant)
            }
        )

    df_depenses = pd.DataFrame(
        data_depenses
    )

    df_pie = (
        df_depenses
        .groupby("Catégorie")
        .sum()
        .reset_index()
    )

    fig = px.pie(
        df_pie,
        names="Catégorie",
        values="Montant",
        title="Répartition des Dépenses"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

else:

    st.info(
        "Aucune dépense enregistrée."
    )

st.divider()

# =====================================================
# EVOLUTION DES REVENUS
# =====================================================

st.subheader("Évolution des Revenus")

revenus = (
    db.query(Revenu)
    .order_by(Revenu.id)
    .all()
)

if revenus:

    data = []

    for i, r in enumerate(revenus):

        data.append(
            {
                "Période": i + 1,
                "Montant": float(r.montant)
            }
        )

    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="Période",
        y="Montant",
        markers=True,
        title="Historique des Revenus"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

else:

    st.info(
        "Aucun revenu enregistré."
    )

st.divider()

# =====================================================
# EVOLUTION DES DEPENSES
# =====================================================

st.subheader("Évolution des Dépenses")

if depenses:

    data = []

    for i, d in enumerate(depenses):

        data.append(
            {
                "Période": i + 1,
                "Montant": float(d.montant)
            }
        )

    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="Période",
        y="Montant",
        title="Historique des Dépenses"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

else:

    st.info(
        "Aucune dépense enregistrée."
    )

st.divider()

# =====================================================
# OBJECTIFS FINANCIERS
# =====================================================

st.subheader("Objectifs Financiers")

objectifs = (
    db.query(Objectif)
    .all()
)

if objectifs:

    for obj in objectifs:

        cible = float(obj.montant_cible or 0)
        actuel = float(obj.montant_actuel or 0)

        progression = 0

        if cible > 0:

            progression = (
                actuel / cible
            )

        st.write(
            f"### {obj.nom}"
        )

        st.progress(
            min(progression, 1.0)
        )

        st.write(
            f"{actuel:,.0f} FCFA / {cible:,.0f} FCFA"
        )

else:

    st.info(
        "Aucun objectif enregistré."
    )

st.divider()

# =====================================================
# TOP 10 DEPENSES
# =====================================================

st.subheader("Top 10 Dépenses")

if depenses:

    data = []

    for d in depenses:

        data.append(
            {
                "Date": d.date_depense,
                "Catégorie": d.categorie,
                "Montant": float(d.montant)
            }
        )

    df_top = pd.DataFrame(data)

    df_top = (
        df_top
        .sort_values(
            by="Montant",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        df_top,
        width="stretch"
    )

else:

    st.info(
        "Aucune dépense enregistrée."
    )

st.divider()

# =====================================================
# SCORE FINANCIER
# =====================================================

st.subheader("Score Financier Familial")

score = 0

if float(total_revenus) > 0:

    score += min(
        (
            float(total_epargne)
            / float(total_revenus)
        ) * 40,
        40
    )

if objectifs:

    score += 30

if solde_net > 0:

    score += 30

score = round(score)

st.metric(
    "Score Financier",
    f"{score}/100"
)

if score >= 70:

    st.success(
        "Situation financière excellente."
    )

elif score >= 50:

    st.warning(
        "Situation financière moyenne."
    )

else:

    st.error(
        "Situation financière à améliorer."
    )

db.close()