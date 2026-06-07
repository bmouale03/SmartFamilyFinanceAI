from sqlalchemy import func

from models.revenu import Revenu
from models.depense import Depense
from models.epargne import Epargne
from models.compte import Compte


class DashboardService:

    def __init__(self, db):
        self.db = db

    def total_revenus(self):

        total = (
            self.db.query(
                func.sum(Revenu.montant)
            )
            .scalar()
        )

        return float(total or 0)

    def total_depenses(self):

        total = (
            self.db.query(
                func.sum(Depense.montant)
            )
            .scalar()
        )

        return float(total or 0)

    def total_epargne(self):

        total = (
            self.db.query(
                func.sum(Epargne.montant)
            )
            .scalar()
        )

        return float(total or 0)

    def patrimoine(self):

        revenus = self.total_revenus()

        depenses = self.total_depenses()

        epargne = self.total_epargne()

        return revenus - depenses + epargne

    def historique(self):

        revenus = (
            self.db.query(Revenu)
            .order_by(Revenu.id)
            .all()
        )

        return revenus