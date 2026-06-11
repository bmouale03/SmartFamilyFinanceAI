
import streamlit as st

from database import Base, engine

# Import des modèles
from models.user import User
from models.compte import Compte
from models.revenu import Revenu
from models.depense import Depense
from models.epargne import Epargne
from models.objectif import Objectif
from models.patrimoine import Patrimoine
# Création automatique des tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("Erreur création tables :", e)

# ==========================
# Configuration générale
# ==========================

st.set_page_config(
    page_title="Smart Family Finance AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# Vérification de session
# ==========================

if "token" not in st.session_state:
    st.switch_page("pages/login.py")

# ==========================
# Décodage JWT
# ==========================

try:

    from jwt_manager import decode_token

    payload = decode_token(
        st.session_state["token"]
    )

except Exception:

    st.session_state.clear()

    st.switch_page(
        "pages/login.py"
    )

# ==========================
# Sidebar
# ==========================

st.sidebar.title(
    "💰 Smart Family Finance AI"
)

st.sidebar.success(
    "Connecté"
)

st.sidebar.write(
    f"👤 {payload['sub']}"
)

st.sidebar.write(
    f"🎯 Rôle : {payload['role']}"
)

st.sidebar.markdown("---")

# ==========================
# Navigation principale
# ==========================

st.sidebar.page_link(
    "pages/dashboard.py",
    label="📊 Dashboard"
)

st.sidebar.page_link(
    "pages/revenus.py",
    label="💰 Revenus"
)

st.sidebar.page_link(
    "pages/depenses.py",
    label="🛒 Dépenses"
)

st.sidebar.page_link(
    "pages/epargne.py",
    label="🏦 Épargne"
)

st.sidebar.page_link(
    "pages/objectifs.py",
    label="🎯 Objectifs"
)

st.sidebar.page_link(
    "pages/rapports.py",
    label="📄 Rapports"
)

st.sidebar.page_link(
    "pages/predictions.py",
    label="🤖 Prévisions IA"
)

st.sidebar.page_link(
    "pages/export_excel.py",
    label="📤 Export Excel"
)

st.sidebar.page_link(
    "pages/export_pdf.py",
    label="📄 Export PDF"
)

# ==========================
# Administration
# ==========================

if payload["role"] == "ADMIN":

    st.sidebar.markdown("---")

    st.sidebar.subheader(
        "Administration"
    )

    st.sidebar.page_link(
        "pages/import_excel.py",
        label="📥 Import Excel"
    )

    st.sidebar.page_link(
        "pages/utilisateurs.py",
        label="👥 Utilisateurs"
    )

# ==========================
# Déconnexion
# ==========================

st.sidebar.markdown("---")

if st.sidebar.button(
    "🚪 Déconnexion"
):

    st.session_state.clear()

    st.switch_page(
        "pages/login.py"
    )

# ==========================
# Page d'accueil
# ==========================

st.title(
    "💰 Smart Family Finance AI"
)

st.markdown(
    """
    Bienvenue dans votre plateforme intelligente
    de gestion financière familiale.
    """
)

st.info(
    """
    Utilisez le menu latéral pour accéder
    aux différentes fonctionnalités.
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        "📊 Tableau de bord financier"
    )

with col2:
    st.info(
        "🏦 Gestion de l'épargne"
    )

with col3:
    st.warning(
        "🤖 Prévisions IA"
    )
    
st.sidebar.page_link(
    "pages/patrimoine.py",
    label="🏠 Patrimoine"
)
st.markdown("---")

st.subheader(
    "Vue d'ensemble"
)

st.write(
    """
    Smart Family Finance AI vous permet de :

    • Suivre vos revenus et dépenses

    • Gérer votre épargne familiale

    • Suivre vos objectifs financiers

    • Importer automatiquement vos budgets Excel

    • Générer des rapports détaillés

    • Obtenir des prévisions financières grâce à l'IA

    • Exporter vos données en Excel et PDF
    """
)

