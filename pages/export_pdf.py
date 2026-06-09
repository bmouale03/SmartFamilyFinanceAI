import streamlit as st
import pandas as pd
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from database import SessionLocal

from models.revenu import Revenu
from models.depense import Depense
from models.epargne import Epargne
from models.objectif import Objectif
import plotly.express as px
from reportlab.platypus import Image

st.set_page_config(
    page_title="Export PDF",
    page_icon="📄",
    layout="wide"
)

st.title(
    "📄 Rapport Financier PDF"
)

db = SessionLocal()


def generer_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = (
        getSampleStyleSheet()
    )

    elements = []

    # =====================
    # Titre
    # =====================

    elements.append(
        Paragraph(
            "Smart Family Finance AI",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # =====================
    # Revenus
    # =====================

    revenus = (
        db.query(Revenu)
        .all()
    )

    total_revenus = sum(
        float(r.montant)
        for r in revenus
    )

    elements.append(
        Paragraph(
            f"Total Revenus : {total_revenus:,.0f} FCFA",
            styles["Heading2"]
        )
    )

    # =====================
    # Dépenses
    # =====================

    depenses = (
        db.query(Depense)
        .all()
    )

    total_depenses = sum(
        float(d.montant)
        for d in depenses
    )

    elements.append(
        Paragraph(
            f"Total Dépenses : {total_depenses:,.0f} FCFA",
            styles["Heading2"]
        )
    )

    # =====================
    # Épargne
    # =====================

    epargnes = (
        db.query(Epargne)
        .all()
    )

    total_epargne = sum(
        float(e.montant)
        for e in epargnes
    )

    elements.append(
        Paragraph(
            f"Total Épargne : {total_epargne:,.0f} FCFA",
            styles["Heading2"]
        )
    )

    # =====================
    # Patrimoine
    # =====================

    patrimoine = (
        total_revenus
        -
        total_depenses
        +
        total_epargne
    )

    elements.append(
        Paragraph(
            f"Patrimoine : {patrimoine:,.0f} FCFA",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # =====================
    # Objectifs
    # =====================

    objectifs = (
        db.query(Objectif)
        .all()
    )

    elements.append(
        Paragraph(
            "Objectifs Financiers",
            styles["Heading1"]
        )
    )

    for obj in objectifs:

        elements.append(
            Paragraph(
                f"{obj.nom} : "
                f"{float(obj.montant_actuel):,.0f} / "
                f"{float(obj.montant_cible):,.0f} FCFA",
                styles["BodyText"]
            )
        )

    elements.append(
        PageBreak()
    )

    # =====================
    # Synthèse
    # =====================

    elements.append(
        Paragraph(
            "Synthèse Financière",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            f"""
            Revenus : {total_revenus:,.0f} FCFA<br/>
            Dépenses : {total_depenses:,.0f} FCFA<br/>
            Épargne : {total_epargne:,.0f} FCFA<br/>
            Patrimoine : {patrimoine:,.0f} FCFA
            """,
            styles["BodyText"]
        )
    )

    doc.build(
        elements
    )

    buffer.seek(0)

    return buffer


if st.button(
    "📄 Générer le PDF"
):

    pdf = generer_pdf()

    st.download_button(
        label="⬇️ Télécharger le PDF",
        data=pdf,
        file_name="SmartFamilyFinance.pdf",
        mime="application/pdf"
    )

    st.success(
        "Rapport PDF généré avec succès."
    )
