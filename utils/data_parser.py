import pandas as pd


class DataParser:
    def __init__(self):
        pass

    def parse(self, data):
        df = pd.DataFrame(data)

        print(df)

        df["price"] = pd.to_numeric(df["price"], errors="coerce", downcast="unsigned")
        df["year"] = pd.to_numeric(df["year"], errors="coerce", downcast="unsigned")
        df["kilometers"] = pd.to_numeric(
            df["kilometers"], errors="coerce", downcast="unsigned"
        )

        return df
