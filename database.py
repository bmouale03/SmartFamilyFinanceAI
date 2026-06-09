from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st
import os

DATABASE_URL = None

# Streamlit Cloud Secrets
if "DATABASE_URL" in st.secrets:
    DATABASE_URL = st.secrets["DATABASE_URL"]

# Fallback local
if DATABASE_URL is None:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://admin:admin123@postgres:5432/smartfamily"
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