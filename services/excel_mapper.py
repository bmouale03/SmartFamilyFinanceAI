class ExcelMapper:

    def identify(
            self,
            sheet_name,
            df
    ):

        columns = [
            str(c).lower()
            for c in df.columns
        ]

        result = {

            "sheet": sheet_name,
            "type": "unknown",
            "data": df
        }

        revenu_keywords = [

            "salaire",
            "revenu",
            "prime",
            "gain"
        ]

        depense_keywords = [

            "loyer",
            "eau",
            "électricité",
            "internet",
            "transport",
            "alimentaire"
        ]

        compte_keywords = [

            "compte",
            "épargne",
            "caisse",
            "tinkoff",
            "cber"
        ]

        text = " ".join(columns)

        if any(
                k in text
                for k in revenu_keywords
        ):

            result["type"] = "revenu"

        elif any(
                k in text
                for k in depense_keywords
        ):

            result["type"] = "depense"

        elif any(
                k in text
                for k in compte_keywords
        ):

            result["type"] = "epargne"

        return result