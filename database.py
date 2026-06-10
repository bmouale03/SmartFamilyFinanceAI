from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
import streamlit as st

DATABASE_URL = st.secrets["DATABASE_URL"]

st.write("Secrets :", list(st.secrets.keys()))

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    st.success("Connexion PostgreSQL OK")

except Exception as e:
    st.error(f"ERREUR POSTGRESQL : {repr(e)}")
    st.stop()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()