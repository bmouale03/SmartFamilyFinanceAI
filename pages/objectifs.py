import streamlit as st
import pandas as pd

from database import SessionLocal
from models.objectif import Objectif

st.set_page_config(
    page_title="Objectifs Financiers",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Gestion des Objectifs Financiers")

db = SessionLocal()

# =====================================
# Chargement des objectifs
# =====================================

objectifs = db.query(Objectif).all()

data = []

for obj in objectifs:

    progression = 0

    if (
        obj.montant_cible
        and float(obj.montant_cible) > 0
    ):

        progression = (
            float(obj.montant_actuel)
            /
            float(obj.montant_cible)
        ) * 100

    data.append(
        {
            "ID": obj.id,
            "Objectif": obj.nom,
            "Description": obj.description,
            "Montant Cible": float(
                obj.montant_cible or 0
            ),
            "Montant Actuel": float(
                obj.montant_actuel or 0
            ),
            "Progression (%)": round(
                progression,
                2
            ),
            "Date Limite": obj.date_limite
        }
    )

df = pd.DataFrame(data)

# =====================================
# KPI
# =====================================

st.metric(
    "Nombre d'Objectifs",
    len(df)
)

# =====================================
# Tableau
# =====================================

st.subheader(
    "Liste des Objectifs"
)

st.dataframe(
    df,
    use_container_width=True,
    height=450
)

st.markdown("---")

# =====================================
# Ajout Objectif
# =====================================

st.subheader(
    "➕ Ajouter un Objectif"
)

with st.form("ajout_objectif"):

    nom = st.text_input(
        "Nom de l'objectif"
    )

    description = st.text_area(
        "Description"
    )

    montant_cible = st.number_input(
        "Montant cible",
        min_value=0.0,
        step=10000.0
    )

    montant_actuel = st.number_input(
        "Montant actuel",
        min_value=0.0,
        step=1000.0
    )

    date_limite = st.date_input(
        "Date limite"
    )

    submit = st.form_submit_button(
        "Ajouter"
    )

    if submit:

        objectif = Objectif(
            nom=nom,
            description=description,
            montant_cible=montant_cible,
            montant_actuel=montant_actuel,
            date_limite=date_limite
        )

        db.add(objectif)

        db.commit()

        st.success(
            "✅ Objectif ajouté avec succès."
        )

        st.rerun()

# =====================================
# Modification
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "✏️ Modifier un Objectif"
    )

    objectif_id = st.selectbox(
        "Choisir un objectif",
        df["ID"]
    )

    objectif = (
        db.query(Objectif)
        .filter(
            Objectif.id == objectif_id
        )
        .first()
    )

    nouveau_nom = st.text_input(
        "Nom",
        value=objectif.nom
    )

    nouvelle_description = st.text_area(
        "Description",
        value=objectif.description or ""
    )

    nouveau_cible = st.number_input(
        "Montant cible",
        value=float(
            objectif.montant_cible or 0
        )
    )

    nouveau_actuel = st.number_input(
        "Montant actuel",
        value=float(
            objectif.montant_actuel or 0
        )
    )

    nouvelle_date = st.date_input(
        "Date limite",
        value=objectif.date_limite
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Mettre à jour"
        ):

            objectif.nom = nouveau_nom

            objectif.description = (
                nouvelle_description
            )

            objectif.montant_cible = (
                nouveau_cible
            )

            objectif.montant_actuel = (
                nouveau_actuel
            )

            objectif.date_limite = (
                nouvelle_date
            )

            db.commit()

            st.success(
                "✅ Objectif mis à jour."
            )

            st.rerun()

    with col2:

        if st.button(
            "🗑️ Supprimer"
        ):

            db.delete(
                objectif
            )

            db.commit()

            st.success(
                "✅ Objectif supprimé."
            )

            st.rerun()

# =====================================
# Progression
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "📈 Progression des Objectifs"
    )

    for _, row in df.iterrows():

        st.write(
            f"🎯 {row['Objectif']}"
        )

        progression = min(
            int(
                row["Progression (%)"]
            ),
            100
        )

        st.progress(
            progression
        )

        st.write(
            f"{row['Progression (%)']} %"
        )

# =====================================
# Graphique
# =====================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "📊 Comparaison des Objectifs"
    )

    graphique = df[
        [
            "Objectif",
            "Montant Actuel"
        ]
    ]

    st.bar_chart(
        graphique.set_index(
            "Objectif"
        )
    )