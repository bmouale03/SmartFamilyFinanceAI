import streamlit as st
import pandas as pd

from database import SessionLocal
from models.revenu import Revenu

st.set_page_config(
    page_title="Gestion des Revenus",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Gestion des Revenus")

db = SessionLocal()

# ==========================
# Chargement des données
# ==========================

revenus = db.query(Revenu).all()

data = []

for r in revenus:

    data.append(
        {
            "ID": r.id,
            "Type": r.type_revenu,
            "Montant": float(r.montant),
            "Commentaire": r.commentaire
        }
    )

df = pd.DataFrame(data)

# ==========================
# Affichage
# ==========================

st.subheader("Liste des revenus")

st.dataframe(
    df,
    use_container_width=True
)

st.markdown("---")

# ==========================
# Ajout revenu
# ==========================

st.subheader("Ajouter un revenu")

with st.form("ajout_revenu"):

    type_revenu = st.text_input(
        "Type de revenu"
    )

    montant = st.number_input(
        "Montant",
        min_value=0.0,
        step=1000.0
    )

    commentaire = st.text_input(
        "Commentaire"
    )

    submit = st.form_submit_button(
        "Ajouter"
    )

    if submit:

        revenu = Revenu(
            type_revenu=type_revenu,
            montant=montant,
            commentaire=commentaire
        )

        db.add(revenu)

        db.commit()

        st.success(
            "Revenu ajouté."
        )

        st.rerun()

# ==========================
# Modification
# ==========================

if len(df) > 0:

    st.markdown("---")

    st.subheader(
        "Modifier un revenu"
    )

    revenu_id = st.selectbox(
        "Choisir un revenu",
        df["ID"]
    )

    revenu = (
        db.query(Revenu)
        .filter(
            Revenu.id == revenu_id
        )
        .first()
    )

    nouveau_type = st.text_input(
        "Type",
        value=revenu.type_revenu
    )

    nouveau_montant = st.number_input(
        "Montant",
        value=float(revenu.montant)
    )

    nouveau_commentaire = st.text_input(
        "Commentaire",
        value=revenu.commentaire or ""
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Mettre à jour"
        ):

            revenu.type_revenu = nouveau_type

            revenu.montant = nouveau_montant

            revenu.commentaire = nouveau_commentaire

            db.commit()

            st.success(
                "Revenu mis à jour."
            )

            st.rerun()

    with col2:

        if st.button(
            "Supprimer"
        ):

            db.delete(revenu)

            db.commit()

            st.success(
                "Revenu supprimé."
            )

            st.rerun()