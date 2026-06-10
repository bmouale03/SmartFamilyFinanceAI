import streamlit as st
import pandas as pd

from database import SessionLocal
from models.depense import Depense

st.set_page_config(
    page_title="Gestion des Dépenses",
    page_icon="🛒",
    layout="wide"
)

st.title("Gestion des Dépenses")

db = SessionLocal()

# =====================================
# Chargement des dépenses
# =====================================

depenses = db.query(Depense).all()

data = []

for d in depenses:

    data.append(
        {
            "ID": d.id,
            "Date": d.date_depense,
            "Catégorie": d.categorie,
            "Montant": float(d.montant),
            "Commentaire": d.commentaire
        }
    )

df = pd.DataFrame(data)

# =====================================
# Statistiques
# =====================================

total_depenses = (
    df["Montant"].sum()
    if not df.empty
    else 0
)

st.metric(
    "Total des Dépenses",
    f"{total_depenses:,.0f} FCFA"
)

# =====================================
# Liste des dépenses
# =====================================

st.subheader("Liste des Dépenses")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

st.markdown("---")

# =====================================
# Ajout d'une dépense
# =====================================

st.subheader("➕ Ajouter une Dépense")

with st.form("ajout_depense"):

    date_depense = st.date_input(
        "Date"
    )

    categorie = st.selectbox(
        "Catégorie",
        [
            "Alimentation",
            "Transport",
            "Logement",
            "Electricité",
            "Internet",
            "Santé",
            "Education",
            "Loisirs",
            "Autres"
        ]
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

        depense = Depense(
            date_depense=date_depense,
            categorie=categorie,
            montant=montant,
            commentaire=commentaire
        )

        db.add(depense)

        db.commit()

        st.success(
            "Dépense ajoutée avec succès."
        )

        st.rerun()

# =====================================
# Modification
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "✏️ Modifier une Dépense"
    )

    depense_id = st.selectbox(
        "Choisir une dépense",
        df["ID"]
    )

    depense = (
        db.query(Depense)
        .filter(
            Depense.id == depense_id
        )
        .first()
    )

    nouvelle_date = st.date_input(
        "Date",
        value=depense.date_depense
    )

    nouvelle_categorie = st.text_input(
        "Catégorie",
        value=depense.categorie
    )

    nouveau_montant = st.number_input(
        "Montant",
        value=float(depense.montant)
    )

    nouveau_commentaire = st.text_input(
        "Commentaire",
        value=depense.commentaire or ""
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Mettre à jour"
        ):

            depense.date_depense = nouvelle_date

            depense.categorie = nouvelle_categorie

            depense.montant = nouveau_montant

            depense.commentaire = nouveau_commentaire

            db.commit()

            st.success(
                "Dépense mise à jour."
            )

            st.rerun()

    with col2:

        if st.button(
            "🗑️ Supprimer"
        ):

            db.delete(depense)

            db.commit()

            st.success(
                "Dépense supprimée."
            )

            st.rerun()

# =====================================
# Analyse rapide
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "📊 Répartition des Dépenses"
    )

    repartition = (
        df.groupby("Catégorie")["Montant"]
        .sum()
        .reset_index()
    )

    st.bar_chart(
        repartition.set_index(
            "Catégorie"
        )
    )