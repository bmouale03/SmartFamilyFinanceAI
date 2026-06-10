from sqlalchemy import *
from database import Base
from datetime import datetime


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nom = Column(
        String(100),
        nullable=False
    )

    prenom = Column(
        String(100)
    )

    email = Column(
        String(150),
        nullable=False,
        unique=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        default="Utilisateur"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )