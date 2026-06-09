from sqlalchemy import *

from database import Base

class Compte(Base):

    __tablename__ = "comptes"

    id = Column(
        Integer,
        primary_key=True
    )

    nom_compte = Column(
        String(100)
    )

    devise = Column(
        String(20)
    )

    solde = Column(
        Numeric(15,2)
    )

    type_compte = Column(
        String(50)
    )