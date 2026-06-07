from sqlalchemy import *

from database import Base

class Epargne(Base):

    __tablename__ = "epargnes"

    id = Column(
        Integer,
        primary_key=True
    )

    mois_budget = Column(
        String(20),
        nullable=True
    )

    compte_id = Column(
        Integer,
        ForeignKey("comptes.id")
    )

    date_operation = Column(Date)

    montant = Column(
        Numeric(15,2)
    )

    observation = Column(Text)