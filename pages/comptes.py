import streamlit as st
import pandas as pd

from database import SessionLocal
from models.compte import Compte

st.set_page_config(
    page_title="Gestion des Comptes",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Gestion des Comptes Bancaires")

db = SessionLocal()

# =====================================
# Chargement des comptes
# =====================================

comptes = db.query(Compte).all()

data = []

for c in comptes:

    data.append(
        {
            "ID": c.id,
            "Compte": c.nom_compte,
            "Devise": c.devise,
            "Solde": float(c.solde),
            "Type": c.type_compte
        }
    )

df = pd.DataFrame(data)

# =====================================
# Indicateurs
# =====================================

solde_total = (
    df["Solde"].sum()
    if not df.empty
    else 0
)

st.metric(
    "💰 Patrimoine Bancaire",
    f"{solde_total:,.0f} FCFA"
)

# =====================================
# Tableau des comptes
# =====================================

st.subheader("Liste des Comptes")

st.dataframe(
    df,
    use_container_width=True,
    height=450
)

st.markdown("---")

# =====================================
# Création d'un compte
# =====================================

st.subheader("➕ Ajouter un Compte")

with st.form("ajout_compte"):

    nom_compte = st.text_input(
        "Nom du compte"
    )

    devise = st.selectbox(
        "Devise",
        [
            "FCFA",
            "RUB",
            "EUR",
            "USD"
        ]
    )

    solde = st.number_input(
        "Solde",
        min_value=0.0,
        step=1000.0
    )

    type_compte = st.selectbox(
        "Type de compte",
        [
            "Compte Courant",
            "Épargne",
            "Investissement",
            "Tinkoff",
            "CBER",
            "Autre"
        ]
    )

    submit = st.form_submit_button(
        "Ajouter"
    )

    if submit:

        compte = Compte(
            nom_compte=nom_compte,
            devise=devise,
            solde=solde,
            type_compte=type_compte
        )

        db.add(compte)

        db.commit()

        st.success(
            "Compte ajouté avec succès."
        )

        st.rerun()

# =====================================
# Modification
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "✏️ Modifier un Compte"
    )

    compte_id = st.selectbox(
        "Choisir un compte",
        df["ID"]
    )

    compte = (
        db.query(Compte)
        .filter(
            Compte.id == compte_id
        )
        .first()
    )

    nouveau_nom = st.text_input(
        "Nom",
        value=compte.nom_compte
    )

    nouvelle_devise = st.selectbox(
        "Devise",
        [
            "FCFA",
            "RUB",
            "EUR",
            "USD"
        ],
        index=0
    )

    nouveau_solde = st.number_input(
        "Solde",
        value=float(compte.solde)
    )

    nouveau_type = st.text_input(
        "Type",
        value=compte.type_compte
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Mettre à jour"
        ):

            compte.nom_compte = nouveau_nom

            compte.devise = nouvelle_devise

            compte.solde = nouveau_solde

            compte.type_compte = nouveau_type

            db.commit()

            st.success(
                "Compte mis à jour."
            )

            st.rerun()

    with col2:

        if st.button(
            "🗑️ Supprimer"
        ):

            db.delete(compte)

            db.commit()

            st.success(
                "Compte supprimé."
            )

            st.rerun()

# =====================================
# Analyse des comptes
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "📊 Répartition des soldes"
    )

    repartition = (
        df.groupby("Type")["Solde"]
        .sum()
        .reset_index()
    )

    st.bar_chart(
        repartition.set_index(
            "Type"
        )
    )

# =====================================
# Comptes stratégiques
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "⭐ Comptes Stratégiques"
    )

    comptes_importants = df[
        df["Compte"].str.contains(
            "Ben|Olivia|Tinkoff|CBER|Epargne",
            case=False,
            na=False
        )
    ]

    st.dataframe(
        comptes_importants,
        use_container_width=True
    )