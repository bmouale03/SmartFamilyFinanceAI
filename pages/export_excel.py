import streamlit as st
import pandas as pd
from io import BytesIO

from database import SessionLocal

from models.revenu import Revenu
from models.depense import Depense
from models.epargne import Epargne
from models.objectif import Objectif
from models.compte import Compte

st.set_page_config(
    page_title="Export Excel",
    page_icon="📤",
    layout="wide"
)

st.title("📤 Export des Données")

db = SessionLocal()

# =====================================
# Fonction Export
# =====================================

def generer_excel():

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # =====================
        # Revenus
        # =====================

        revenus = db.query(Revenu).all()

        revenus_df = pd.DataFrame([
            {
                "ID": r.id,
                "Type": r.type_revenu,
                "Montant": float(r.montant),
                "Commentaire": r.commentaire
            }
            for r in revenus
        ])

        revenus_df.to_excel(
            writer,
            sheet_name="Revenus",
            index=False
        )

        # =====================
        # Dépenses
        # =====================

        depenses = db.query(Depense).all()

        depenses_df = pd.DataFrame([
            {
                "ID": d.id,
                "Date": d.date_depense,
                "Categorie": d.categorie,
                "Montant": float(d.montant),
                "Commentaire": d.commentaire
            }
            for d in depenses
        ])

        depenses_df.to_excel(
            writer,
            sheet_name="Depenses",
            index=False
        )

        # =====================
        # Comptes
        # =====================

        comptes = db.query(Compte).all()

        comptes_df = pd.DataFrame([
            {
                "ID": c.id,
                "Compte": c.nom_compte,
                "Devise": c.devise,
                "Solde": float(c.solde),
                "Type": c.type_compte
            }
            for c in comptes
        ])

        comptes_df.to_excel(
            writer,
            sheet_name="Comptes",
            index=False
        )

        # =====================
        # Epargne
        # =====================

        epargnes = db.query(Epargne).all()

        epargnes_df = pd.DataFrame([
            {
                "ID": e.id,
                "Mois": e.mois_budget,
                "Date": e.date_operation,
                "Montant": float(e.montant),
                "Observation": e.observation
            }
            for e in epargnes
        ])

        epargnes_df.to_excel(
            writer,
            sheet_name="Epargne",
            index=False
        )

        # =====================
        # Objectifs
        # =====================

        objectifs = db.query(Objectif).all()

        objectifs_df = pd.DataFrame([
            {
                "ID": o.id,
                "Nom": o.nom,
                "Description": o.description,
                "Montant Cible": float(
                    o.montant_cible or 0
                ),
                "Montant Actuel": float(
                    o.montant_actuel or 0
                ),
                "Date Limite": o.date_limite
            }
            for o in objectifs
        ])

        objectifs_df.to_excel(
            writer,
            sheet_name="Objectifs",
            index=False
        )

    output.seek(0)

    return output

# =====================================
# Interface
# =====================================

st.info(
    "Exporter toutes les données vers un fichier Excel."
)

if st.button(
    "📥 Générer le fichier Excel"
):

    fichier = generer_excel()

    st.download_button(
        label="⬇️ Télécharger Excel",
        data=fichier,
        file_name="SmartFamilyFinance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success(
        "Fichier Excel généré avec succès."
    )