from sqlalchemy import *

from database import Base

class Devise(Base):

    __tablename__ = "devises"

    id = Column(
        Integer,
        primary_key=True
    )

    code = Column(
        String(10)
    )

    nom = Column(
        String(100)
    )

    taux_fcfa = Column(
        Numeric(15,4)
    )