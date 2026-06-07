import pandas as pd

from services.excel_mapper import ExcelMapper


class ExcelParser:

    def __init__(self):

        self.mapper = ExcelMapper()

    def analyse_sheet(
            self,
            sheet_name,
            df
    ):

        return self.mapper.identify(
            sheet_name,
            df
        )