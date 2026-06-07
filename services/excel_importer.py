import pandas as pd

from services.excel_parser import ExcelParser
from services.excel_loader import ExcelLoader


class ExcelImporter:

    def __init__(self, db):

        self.db = db

        self.parser = ExcelParser()

        self.loader = ExcelLoader(db)

    def import_file(self, file_path):

        workbook = pd.ExcelFile(file_path)

        for sheet in workbook.sheet_names:

            dataframe = pd.read_excel(
                file_path,
                sheet_name=sheet
            )

            result = self.parser.analyse_sheet(
                sheet,
                dataframe
            )

            self.loader.load(result)

        return True
import streamlit as st

from database import SessionLocal

from services.excel_importer import (
    ExcelImporter
)

st.title(
    "Import Budget Familial"
)

uploaded_file = st.file_uploader(
    "Importer Excel",
    type=["xlsx"]
)

if uploaded_file:

    with open(
            "temp.xlsx",
            "wb"
    ) as f:

        f.write(
            uploaded_file.read()
        )

    db = SessionLocal()

    importer = ExcelImporter(db)

    importer.import_file(
        "temp.xlsx"
    )

    st.success(
        "Import terminé."
    )