import streamlit as st
import plotly.express as px
from database import SessionLocal
from services.dashboard_service import DashboardService

# Connexion à la base
db = SessionLocal()

# Création du service
service = DashboardService(db)

# ==========================
# BLOC 1 : Calcul des KPI
# ==========================

revenus = service.total_revenus()

depenses = service.total_depenses()

epargne = service.total_epargne()

patrimoine = service.patrimoine()

# ==========================
# Affichage
# ==========================

st.title("📊 Smart Family Finance AI")

# ==========================
# BLOC 2 : Affichage KPI
# ==========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenus",
    f"{revenus:,.0f} FCFA"
)

col2.metric(
    "Dépenses",
    f"{depenses:,.0f} FCFA"
)

col3.metric(
    "Épargne",
    f"{epargne:,.0f} FCFA"
)

col4.metric(
    "Patrimoine",
    f"{patrimoine:,.0f} FCFA"
)
history = service.historique()
