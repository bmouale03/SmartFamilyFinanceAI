from sqlalchemy import *

from database import Base

class Depense(Base):

    __tablename__ = "depenses"

    id = Column(
        Integer,
        primary_key=True
    )

    mois_budget = Column(
        String(20),
        nullable=True
    )

    membre_id = Column(
        Integer,
        nullable=True
    )

    date_depense = Column(
        Date,
        nullable=True
    )

    categorie = Column(
        String(100)
    )

    montant = Column(
        Numeric(15,2),
        default=0
    )

    commentaire = Column(Text)