
import streamlit as st

from database import SessionLocal
from services.budget_importer import BudgetImporter


st.title("📥 Import Budget Familial")

if st.button("Importer le fichier Excel"):

    db = SessionLocal()

    importer = BudgetImporter(db)

    importer.import_budget(
        "data/Budjet-Familial-MOUALE.xlsx"
    )

    st.success(
        "Import terminé avec succès."
    )