from sqlalchemy import *

from database import Base

class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key=True
    )

    date_prediction = Column(Date)

    type_prediction = Column(
        String(100)
    )

    valeur = Column(
        Numeric(15,2)
    )