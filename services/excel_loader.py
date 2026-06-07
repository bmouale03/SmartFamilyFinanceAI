from models.revenu import Revenu
from models.depense import Depense
from models.epargne import Epargne


class ExcelLoader:

    def __init__(self, db):

        self.db = db

    def load(self, result):

        if result["type"] == "revenu":

            self.load_revenus(
                result["data"]
            )

        elif result["type"] == "depense":

            self.load_depenses(
                result["data"]
            )

        elif result["type"] == "epargne":

            self.load_epargne(
                result["data"]
            )
def load_revenus(self, df):

    for _, row in df.iterrows():

        revenu = Revenu(

            type_revenu=
            row.get(
                "Type",
                "Salaire"
            ),

            montant=
            float(
                row.get(
                    "Montant",
                    0
                )
            )
        )

        self.db.add(revenu)

    self.db.commit()
def load_depenses(self, df):

    for _, row in df.iterrows():

        depense = Depense(

            categorie=
            row.get(
                "Catégorie",
                "Divers"
            ),

            montant=
            float(
                row.get(
                    "Montant",
                    0
                )
            )
        )

        self.db.add(depense)

    self.db.commit()
def load_epargne(self, df):

    for _, row in df.iterrows():

        epargne = Epargne(

            montant=
            float(
                row.get(
                    "Montant",
                    0
                )
            )
        )

        self.db.add(
            epargne
        )

    self.db.commit()