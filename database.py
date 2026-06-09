from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st

st.write("=== TEST SECRET ===")

try:
    DATABASE_URL = st.secrets["DATABASE_URL"]
    st.write("SECRET TROUVÉ")
    st.write(DATABASE_URL[:40] + "...")
except Exception as e:
    st.error(f"SECRET INTROUVABLE : {e}")
    raise

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