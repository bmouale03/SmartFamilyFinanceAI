class HistoryBuilder:

    def build_monthly_history(
            self,
            dataframe
    ):

        history = []

        for month in dataframe.columns:

            history.append({

                "month": month,

                "revenus":
                self.extract_revenus(
                    dataframe,
                    month
                ),

                "depenses":
                self.extract_depenses(
                    dataframe,
                    month
                ),

                "epargne":
                self.extract_epargne(
                    dataframe,
                    month
                )
            })

        return history