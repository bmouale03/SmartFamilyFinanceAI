import pandas as pd
from sklearn.linear_model import LinearRegression
from models.revenu import Revenu
from datetime import date
from models.prediction import Prediction

class PredictionService:

    def __init__(self, db):

        self.db = db

    def prevoir_revenus(self):

        revenus = (
            self.db.query(Revenu)
            .order_by(Revenu.id)
            .all()
        )

        if len(revenus) < 2:

            return None

        data = []

        for i, r in enumerate(revenus):

            data.append(
                {
                    "mois": i + 1,
                    "montant": float(r.montant)
                }
            )

        df = pd.DataFrame(data)

        X = df[["mois"]]

        y = df["montant"]

        model = LinearRegression()

        model.fit(X, y)

        prochain_mois = (
            len(df) + 1
        )

        prediction = model.predict(
            [[prochain_mois]]
        )[0]

        return {
            "prochain_mois": prochain_mois,
            "prediction": prediction
        }
prediction = Prediction(

    date_prediction=date.today(),

    type_prediction="Revenus",

    horizon="1 mois",

    valeur_predite=prediction_1,

    modele_utilise="LinearRegression",

    commentaire="Prévision automatique IA"
)

self.db.add(prediction)

self.db.commit()