from sqlalchemy import *

from database import Base


class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key=True
    )

    date_prediction = Column(
        Date
    )

    type_prediction = Column(
        String(100)
    )

    horizon = Column(
        String(50)
    )

    valeur_predite = Column(
        Numeric(15, 2)
    )

    modele_utilise = Column(
        String(100)
    )

    precision_modele = Column(
        Numeric(5, 2),
        nullable=True
    )

    commentaire = Column(
        Text,
        nullable=True
    )