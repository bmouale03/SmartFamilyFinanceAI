import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.linear_model import LinearRegression

from database import SessionLocal
from models.revenu import Revenu
from models.depense import Depense
from models.epargne import Epargne

# ==========================================
# Configuration
# ==========================================

st.set_page_config(
    page_title="Prévisions IA",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Prévisions IA")

st.markdown(
    """
    Analyse prédictive des finances familiales.
    """
)

# ==========================================
# Connexion Base
# ==========================================

db = SessionLocal()

# ==========================================
# Chargement Revenus
# ==========================================

revenus = (
    db.query(Revenu)
    .order_by(Revenu.id)
    .all()
)

if len(revenus) < 2:

    st.warning(
        """
        Au moins deux revenus sont nécessaires
        pour générer des prévisions.
        """
    )

    st.stop()

# ==========================================
# Construction Dataset
# ==========================================

data = []

for i, revenu in enumerate(revenus):

    data.append(
        {
            "Mois": i + 1,
            "Montant": float(
                revenu.montant
            )
        }
    )

df = pd.DataFrame(data)

# ==========================================
# Entraînement IA
# ==========================================

X = df[["Mois"]]

y = df["Montant"]

model = LinearRegression()

model.fit(X, y)

# ==========================================
# Prévisions
# ==========================================

mois_suivant = len(df) + 1

prediction_1 = model.predict(
    pd.DataFrame(
        {"Mois": [mois_suivant]}
    )
)[0]

prediction_3 = model.predict(
    pd.DataFrame(
        {"Mois": [len(df) + 3]}
    )
)[0]

prediction_6 = model.predict(
    pd.DataFrame(
        {"Mois": [len(df) + 6]}
    )
)[0]

prediction_12 = model.predict(
    pd.DataFrame(
        {"Mois": [len(df) + 12]}
    )
)[0]

# ==========================================
# KPI Prévisions
# ==========================================

st.subheader(
    "🔮 Prévisions financières"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Prochain mois",
    f"{prediction_1:,.0f} FCFA"
)

col2.metric(
    "Dans 3 mois",
    f"{prediction_3:,.0f} FCFA"
)

col3.metric(
    "Dans 6 mois",
    f"{prediction_6:,.0f} FCFA"
)

col4.metric(
    "Dans 12 mois",
    f"{prediction_12:,.0f} FCFA"
)

# ==========================================
# Historique
# ==========================================

st.markdown("---")

st.subheader(
    "📋 Historique des revenus"
)

st.dataframe(
    df,
    width="stretch"
)

# ==========================================
# Graphique Historique
# ==========================================

st.markdown("---")

st.subheader(
    "📈 Évolution des revenus"
)

future_df = pd.DataFrame(
    {
        "Mois": [
            len(df) + 1,
            len(df) + 3,
            len(df) + 6,
            len(df) + 12
        ],
        "Montant": [
            prediction_1,
            prediction_3,
            prediction_6,
            prediction_12
        ]
    }
)

historique = df.copy()

historique["Type"] = "Historique"

future_df["Type"] = "Prévision"

graph_df = pd.concat(
    [
        historique,
        future_df
    ]
)

fig = px.line(
    graph_df,
    x="Mois",
    y="Montant",
    color="Type",
    markers=True,
    title="Historique et Prévisions"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ==========================================
# Analyse financière
# ==========================================

st.markdown("---")

st.subheader(
    "📊 Analyse Financière"
)

total_revenus = sum(
    float(r.montant)
    for r in revenus
)

depenses = (
    db.query(Depense)
    .all()
)

total_depenses = sum(
    float(d.montant)
    for d in depenses
)

epargnes = (
    db.query(Epargne)
    .all()
)

total_epargne = sum(
    float(e.montant)
    for e in epargnes
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenus",
    f"{total_revenus:,.0f} FCFA"
)

col2.metric(
    "Total Dépenses",
    f"{total_depenses:,.0f} FCFA"
)

col3.metric(
    "Total Épargne",
    f"{total_epargne:,.0f} FCFA"
)

# ==========================================
# Score Financier
# ==========================================

st.markdown("---")

st.subheader(
    "🏆 Score Financier"
)

if total_revenus > 0:

    taux_epargne = (
        total_epargne
        /
        total_revenus
    ) * 100

else:

    taux_epargne = 0

score = min(
    100,
    round(
        taux_epargne * 2
    )
)

st.progress(
    score / 100
)

st.metric(
    "Score",
    f"{score}/100"
)

# ==========================================
# Recommandations IA
# ==========================================

st.markdown("---")

st.subheader(
    "🤖 Recommandations IA"
)

if score >= 80:

    st.success(
        """
        Situation financière excellente.

        Continuez votre stratégie
        d'épargne actuelle.
        """
    )

elif score >= 50:

    st.warning(
        """
        Situation financière correcte.

        Essayez d'augmenter votre
        taux d'épargne.
        """
    )

else:

    st.error(
        """
        Niveau d'épargne faible.

        Réduisez certaines dépenses
        non essentielles.
        """
    )

# ==========================================
# Tableau Prévisions
# ==========================================

st.markdown("---")

st.subheader(
    "📅 Prévisions Futures"
)

previsions = pd.DataFrame(
    {
        "Horizon": [
            "1 mois",
            "3 mois",
            "6 mois",
            "12 mois"
        ],
        "Prévision FCFA": [
            round(prediction_1),
            round(prediction_3),
            round(prediction_6),
            round(prediction_12)
        ]
    }
)

st.dataframe(
    previsions,
    width="stretch"
)