from pathlib import Path
import pandas as pd

from models import ProductInput


class ExcelLoader:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def load_products(self):
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Excel file not found:\n{self.file_path}"
            )

        df = pd.read_excel(
            self.file_path,
            dtype=str
        ).fillna("")

        # Normalize column names
        df.columns = [
            str(col).strip().lower()
            for col in df.columns
        ]

        asin_column = None
        competitor_column = None

        for col in df.columns:

            if col in ["asin", "amazon asin", "amazon_asin"]:
                asin_column = col

            if col in [
                "competitor url",
                "competitor_url",
                "competitorurl",
                "url"
            ]:
                competitor_column = col

        if not asin_column:
            raise ValueError(
                "ASIN column not found in Excel.\n"
                "Expected: ASIN"
            )

        if not competitor_column:
            raise ValueError(
                "Competitor URL column not found in Excel.\n"
                "Expected: Competitor URL"
            )

        products = []

        for _, row in df.iterrows():

            asin = str(row[asin_column]).strip()
            competitor_url = str(row[competitor_column]).strip()

            if not asin:
                continue

            products.append(
                ProductInput(
                    asin=asin,
                    competitor_url=competitor_url
                )
            )

        return products