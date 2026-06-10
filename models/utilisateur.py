import streamlit as st
import pandas as pd

from datetime import datetime

from database import SessionLocal
from models.user import User

db = SessionLocal()

st.title("👥 Gestion des Utilisateurs")

# ==========================
# AJOUT D'UN UTILISATEUR
# ==========================

with st.expander("➕ Ajouter un utilisateur"):

    nom = st.text_input("Nom")

    prenom = st.text_input("Prénom")

    email = st.text_input("Email")

    mot_de_passe = st.text_input(
        "Mot de passe",
        type="password"
    )

    role = st.selectbox(
        "Rôle",
        [
            "Administrateur",
            "Parent",
            "Enfant",
            "Utilisateur"
        ]
    )

    if st.button("Enregistrer l'utilisateur"):

        existe = (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

        if existe:

            st.error(
                "Cet email existe déjà."
            )

        else:

            utilisateur = User(
                nom=nom,
                prenom=prenom,
                email=email,
                password_hash=mot_de_passe,
                role=role,
                created_at=datetime.now()
            )

            db.add(utilisateur)

            db.commit()

            st.success(
                "Utilisateur ajouté avec succès."
            )

            st.rerun()

# ==========================
# LISTE DES UTILISATEURS
# ==========================

st.subheader("📋 Liste des utilisateurs")

utilisateurs = (
    db.query(User)
    .all()
)

data = []

for u in utilisateurs:

    data.append(
        {
            "ID": u.id,
            "Nom": u.nom,
            "Prénom": u.prenom,
            "Email": u.email,
            "Rôle": u.role,
            "Créé le": u.created_at
        }
    )

df = pd.DataFrame(data)

if not df.empty:

    st.dataframe(
        df,
        width="stretch"
    )

else:

    st.info(
        "Aucun utilisateur enregistré."
    )

# ==========================
# MODIFICATION
# ==========================

st.subheader("✏️ Modifier un utilisateur")

if utilisateurs:

    utilisateur_id = st.selectbox(
        "Choisir un utilisateur",
        [u.id for u in utilisateurs]
    )

    utilisateur = (
        db.query(User)
        .filter(
            User.id == utilisateur_id
        )
        .first()
    )

    nouveau_nom = st.text_input(
        "Nom",
        value=utilisateur.nom,
        key="edit_nom"
    )

    nouveau_prenom = st.text_input(
        "Prénom",
        value=utilisateur.prenom or "",
        key="edit_prenom"
    )

    nouveau_email = st.text_input(
        "Email",
        value=utilisateur.email,
        key="edit_email"
    )

    liste_roles = [
        "Administrateur",
        "Parent",
        "Enfant",
        "Utilisateur"
    ]

    index_role = (
        liste_roles.index(utilisateur.role)
        if utilisateur.role in liste_roles
        else 0
    )

    nouveau_role = st.selectbox(
        "Rôle",
        liste_roles,
        index=index_role,
        key="edit_role"
    )

    if st.button("Mettre à jour"):

        utilisateur.nom = nouveau_nom
        utilisateur.prenom = nouveau_prenom
        utilisateur.email = nouveau_email
        utilisateur.role = nouveau_role

        db.commit()

        st.success(
            "Utilisateur mis à jour."
        )

        st.rerun()

# ==========================
# SUPPRESSION
# ==========================

st.subheader("🗑️ Supprimer un utilisateur")

if utilisateurs:

    id_suppr = st.selectbox(
        "Utilisateur à supprimer",
        [u.id for u in utilisateurs],
        key="supprimer"
    )

    if st.button("Supprimer l'utilisateur"):

        utilisateur = (
            db.query(User)
            .filter(
                User.id == id_suppr
            )
            .first()
        )

        db.delete(utilisateur)

        db.commit()

        st.success(
            "Utilisateur supprimé."
        )

        st.rerun()

# ==========================
# STATISTIQUES
# ==========================

st.subheader("📊 Statistiques")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Nombre d'utilisateurs",
        len(utilisateurs)
    )

with col2:

    nb_admin = len(
        [
            u for u in utilisateurs
            if u.role == "Administrateur"
        ]
    )

    st.metric(
        "Administrateurs",
        nb_admin
    )