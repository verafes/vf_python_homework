import pandas as pd
import os

# Task 6
class DFPlus(pd.DataFrame):
    @property
    def _constructor(self):
        return DFPlus

    @classmethod
    def from_csv(cls, filepath, **kwargs):
        """Creates a DFPlus instance from a CSV file."""
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return cls()

        try:
            df = pd.read_csv(filepath, **kwargs)
            if df.empty:
                print("Warning: The CSV file is empty.")
            return cls(df)
        except Exception as e:
            print(f"Error reading the CSV file: {e}")
            return cls()

    def print_with_headers(self):
        """Prints the DataFrame with headers every 10 rows."""
        total_rows = len(self)
        for start in range(0, total_rows, 10):
            end = start + 10

            # print(self.columns.to_list())
            print(super().iloc[start:end].to_string(index=False))
            print('-' * 50)

if __name__ == "__main__":
    dfp = DFPlus.from_csv("../csv/products.csv")
    dfp.print_with_headers()