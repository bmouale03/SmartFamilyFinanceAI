from sqlalchemy import Column, Integer, String, Date, Numeric, Text

from database import Base


class Revenu(Base):

    __tablename__ = "revenus"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    mois_budget = Column(
        String(20),
        nullable=True
    )

    membre_id = Column(
        Integer,
        nullable=True
    )

    date_revenu = Column(
        Date,
        nullable=True
    )

    type_revenu = Column(
        String(100),
        nullable=True
    )

    montant = Column(
        Numeric(15, 2),
        nullable=False,
        default=0
    )

    commentaire = Column(
        Text,
        nullable=True
    )