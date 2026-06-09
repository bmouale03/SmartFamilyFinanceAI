from sqlalchemy import *

from database import Base


class Depense(Base):

    __tablename__ = "depenses"

    id = Column(
        Integer,
        primary_key=True
    )

    membre_id = Column(
        Integer,
        nullable=True
    )

    date_depense = Column(Date)

    categorie = Column(
        String(100)
    )

    montant = Column(
        Numeric(15, 2)
    )

    commentaire = Column(Text)