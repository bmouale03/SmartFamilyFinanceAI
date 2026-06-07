class CurrencyService:

    def __init__(self):

        self.rub_to_fcfa = 6.85

    def rub_to_fcfa_convert(
            self,
            amount
    ):

        return amount * self.rub_to_fcfa

currency = CurrencyService()

solde_fcfa = (
    currency.rub_to_fcfa_convert(
        250000
    )
)