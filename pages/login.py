import streamlit as st
from database import SessionLocal
from services.auth_service import AuthService

st.set_page_config(
    page_title="Connexion",
    page_icon="🔐"
)

st.title("🔐 Connexion")

email = st.text_input(
    "Email"
)

password = st.text_input(
    "Mot de passe",
    type="password"
)

if st.button("Se connecter"):

    db = SessionLocal()

    try:

        # Normalisation de l'email
        email = email.strip().lower()

        token = AuthService.authenticate_user(
            db,
            email,
            password
        )

        if token:

            st.session_state["token"] = token

            st.success(
                "Connexion réussie..."
            )

            st.switch_page(
                "app.py"
            )

        else:

            st.error(
                "Email ou mot de passe incorrect."
            )

    except Exception as e:

        st.error(
            f"Erreur de connexion : {str(e)}"
        )

    finally:

        db.close()