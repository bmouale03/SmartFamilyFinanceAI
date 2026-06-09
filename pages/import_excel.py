import streamlit as st
import pandas as pd

from database import SessionLocal
from services.budget_importer import BudgetImporter

# =====================================
# Configuration page
# =====================================

st.set_page_config(
    page_title="Import Budget Familial",
    page_icon="📥",
    layout="wide"
)

# =====================================
# Titre
# =====================================

st.title("📥 Import Budget Familial")

st.markdown(
    """
    Cette page permet :

    - d'importer le fichier Excel du budget familial ;
    - d'enregistrer les données dans PostgreSQL ;
    - de visualiser le contenu des feuilles Excel.
    """
)

# =====================================
# Chemin du fichier
# =====================================

FICHIER_EXCEL = (
    "data/Budjet-Familial-MOUALE.xlsx"
)

# =====================================
# Bouton Import
# =====================================

if st.button(
    "📥 Importer le fichier Excel",
    type="primary"
):

    try:

        db = SessionLocal()

        importer = BudgetImporter(db)

        importer.import_budget(
            FICHIER_EXCEL
        )

        st.success(
            "✅ Import terminé avec succès."
        )

    except Exception as e:

        st.error(
            f"❌ Erreur lors de l'import : {e}"
        )

# =====================================
# Lecture du fichier Excel
# =====================================

try:

    xls = pd.ExcelFile(
        FICHIER_EXCEL
    )

    st.markdown("---")

    st.subheader(
        "📑 Feuilles détectées"
    )

    st.write(
        xls.sheet_names
    )

    # ==============================
    # Sélection de feuille
    # ==============================

    feuille = st.selectbox(
        "Choisir une feuille",
        xls.sheet_names
    )

    # ==============================
    # Chargement de la feuille
    # ==============================

    df = pd.read_excel(
        FICHIER_EXCEL,
        sheet_name=feuille,
        header=None
    )

    st.markdown("---")

    st.subheader(
        f"📄 Aperçu : {feuille}"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Nombre de lignes",
        len(df)
    )

    col2.metric(
        "Nombre de colonnes",
        len(df.columns)
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=700
    )

except Exception as e:

    st.warning(
        f"Impossible de lire le fichier Excel : {e}"
    )