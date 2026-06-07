import streamlit as st

from jwt_manager import decode_token

def require_auth():

    if "token" not in st.session_state:

        st.warning(
            "Veuillez vous connecter."
        )

        st.stop()

    try:

        payload = decode_token(
            st.session_state[
                "token"
            ]
        )

        return payload

    except:

        st.error(
            "Session expirée."
        )

        st.stop()