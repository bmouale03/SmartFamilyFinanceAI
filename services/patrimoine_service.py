from services.currency_service import CurrencyService

class PatrimoineService:

    def __init__(self, db):

        self.db = db

        self.currency = CurrencyService()

    def patrimoine_total(self):

        comptes_fcfa = 0
        comptes_rub = 0

        comptes = self.db.query(
            Compte
        ).all()

        for compte in comptes:

            if compte.devise == "FCFA":

                comptes_fcfa += compte.solde

            elif compte.devise == "RUB":

                comptes_rub += (
                    self.currency
                    .rub_to_fcfa_convert(
                        compte.solde
                    )
                )

        return comptes_fcfa + comptes_rub