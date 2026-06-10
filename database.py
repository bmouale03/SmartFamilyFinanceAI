from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import streamlit as st

try:
    if "DATABASE_URL" in st.secrets:
        DATABASE_URL = st.secrets["DATABASE_URL"]
        st.write("✅ DATABASE_URL trouvée dans les Secrets")
    else:
        DATABASE_URL = os.getenv("DATABASE_URL")
        st.write("⚠️ DATABASE_URL trouvée dans les variables d'environnement")

except Exception as e:
    st.error(f"Erreur Secrets : {e}")
    DATABASE_URL = os.getenv("DATABASE_URL")

st.write("Secrets disponibles :", list(st.secrets.keys()))

if not DATABASE_URL:
    raise Exception(
        "DATABASE_URL non configurée"
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()