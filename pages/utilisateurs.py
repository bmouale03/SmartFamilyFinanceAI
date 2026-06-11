import streamlit as st
import pandas as pd
from datetime import datetime

from database import SessionLocal
from models.user import User
from security import hash_password

db = SessionLocal()

st.title("👥 Gestion des Utilisateurs")

# =====================================================
# AJOUT D'UN UTILISATEUR
# =====================================================

with st.expander("➕ Ajouter un utilisateur"):

    nom = st.text_input(
        "Nom",
        key="add_nom"
    )

    prenom = st.text_input(
        "Prénom",
        key="add_prenom"
    )

    email = st.text_input(
        "Email",
        key="add_email"
    )

    mot_de_passe = st.text_input(
        "Mot de passe",
        type="password",
        key="add_password"
    )

    role = st.selectbox(
        "Rôle",
        [
            "Administrateur",
            "Parent",
            "Enfant",
            "Utilisateur"
        ],
        key="add_role"
    )

    if st.button(
        "Enregistrer l'utilisateur",
        key="btn_add_user"
    ):

        email = email.strip().lower()

        if not nom or not email or not mot_de_passe:

            st.error(
                "Veuillez renseigner tous les champs obligatoires."
            )

        else:

            existe = (
                db.query(User)
                .filter(User.email == email)
                .first()
            )

            if existe:

                st.error(
                    "Cet email existe déjà."
                )

            else:

                mot_de_passe_hash = hash_password(
                    mot_de_passe
                )

                utilisateur = User(
                    nom=nom.strip(),
                    prenom=prenom.strip(),
                    email=email,
                    password_hash=mot_de_passe_hash,
                    role=role,
                    created_at=datetime.now()
                )

                db.add(utilisateur)

                db.commit()

                db.refresh(utilisateur)

                st.success(
                    "Utilisateur ajouté avec succès."
                )

                st.rerun()

# =====================================================
# LISTE DES UTILISATEURS
# =====================================================

st.subheader("📋 Liste des utilisateurs")

utilisateurs = (
    db.query(User)
    .order_by(User.id)
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

# =====================================================
# MODIFICATION
# =====================================================

st.subheader("✏️ Modifier un utilisateur")

if utilisateurs:

    utilisateur_id = st.selectbox(
        "Choisir un utilisateur",
        [u.id for u in utilisateurs],
        key="edit_user"
    )

    utilisateur = (
        db.query(User)
        .filter(User.id == utilisateur_id)
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

    roles = [
        "Administrateur",
        "Parent",
        "Enfant",
        "Utilisateur"
    ]

    index_role = (
        roles.index(utilisateur.role)
        if utilisateur.role in roles
        else 0
    )

    nouveau_role = st.selectbox(
        "Rôle",
        roles,
        index=index_role,
        key="edit_role"
    )

    if st.button(
        "Mettre à jour",
        key="btn_update_user"
    ):

        utilisateur.nom = nouveau_nom.strip()
        utilisateur.prenom = nouveau_prenom.strip()
        utilisateur.email = nouveau_email.strip().lower()
        utilisateur.role = nouveau_role

        db.commit()

        st.success(
            "Utilisateur mis à jour."
        )

        st.rerun()

# =====================================================
# SUPPRESSION
# =====================================================

st.subheader("🗑️ Supprimer un utilisateur")

if utilisateurs:

    id_suppr = st.selectbox(
        "Utilisateur à supprimer",
        [u.id for u in utilisateurs],
        key="delete_user"
    )

    if st.button(
        "Supprimer l'utilisateur",
        key="btn_delete_user"
    ):

        utilisateur = (
            db.query(User)
            .filter(User.id == id_suppr)
            .first()
        )

        if utilisateur:

            db.delete(utilisateur)

            db.commit()

            st.success(
                "Utilisateur supprimé."
            )

            st.rerun()

# =====================================================
# STATISTIQUES
# =====================================================

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
            u
            for u in utilisateurs
            if u.role == "Administrateur"
        ]
    )

    st.metric(
        "Administrateurs",
        nb_admin
    )

db.close()
