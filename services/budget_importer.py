import pandas as pd

from models.revenu import Revenu


class BudgetImporter:

    def __init__(self, db):
        self.db = db

    def import_budget(self, file_path):

        xls = pd.ExcelFile(file_path)

        for sheet in xls.sheet_names:

            try:

                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet,
                    header=None
                )

                valeur = df.iloc[10, 17]

                if pd.notna(valeur):

                    revenu_total = float(valeur)

                    revenu = Revenu(
                        type_revenu="Revenu Mensuel",
                        montant=revenu_total
                    )

                    self.db.add(revenu)

                    print(
                        f"{sheet} -> {revenu_total}"
                    )

            except Exception as e:

                print(
                    f"Erreur feuille {sheet}: {e}"
                )

        self.db.commit()

        print(
            "Import terminé."
        )