import pandas as pd
import os
from hackathon.paths import EVALUATION_DIR


def verify(df, print_errors=False):
    df_solution = pd.read_excel(
        os.path.join(EVALUATION_DIR, "solution_location_country_mapping.xlsx")
    )

    result = df_solution["country"] == df["country"]

    print(f"Correctly inferred countries: {result.sum()} out of {len(result)}")

    if result.sum() == len(result):
        print("Weeey, you did it! :)")
    elif print_errors:
        print("Errors:")
        for i, row in df_solution.iterrows():
            if row["country"] != df.loc[i, "country"]:
                print(f"Row {i}: {row['location']} -> {df.loc[i, 'country']} (correct: {row['country']})")  # noqa E501
