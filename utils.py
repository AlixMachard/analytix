import pandas as pd
from typing import List


def preprocess_csv_data(file_paths: List[str]) -> pd.DataFrame:
    """Load and concatenate CSV files after dropping 'Unnamed: 0' column."""
    df_list = []
    for file_path in file_paths:
        df = pd.read_csv(file_path).drop(columns="Unnamed: 0")
        df_list.append(df)
    dftotal = pd.concat(df_list)
    # dftotal[["year", "month", "day"]] = dftotal["day"].str.split("-", expand=True)
    # month_names = {
    #     str(i).zfill(2): month
    #     for i, month in enumerate(
    #         [
    #             "January",
    #             "February",
    #             "March",
    #             "April",
    #             "May",
    #             "June",
    #             "July",
    #             "August",
    #             "September",
    #             "October",
    #             "November",
    #             "December",
    #         ],
    #         start=1,
    #     )
    # }
    # dftotal["month"] = dftotal["month"].map(month_names)
    dftotal.fillna(0)
    return dftotal


def setup_data() -> pd.DataFrame:
    data_files = [
        "prod_2023/prod_01_2023.csv",
        "prod_2023/prod_02_2023.csv",
        "prod_2023/prod_03_2023.csv",
        "prod_2023/prod_04_2023.csv",
        # "prod_2023/prod_05_2023.csv",
        # "prod_2023/prod_06_2023.csv",
        # "prod_2023/prod_07_2023.csv",
        # "prod_2023/prod_08_2023.csv",
        # "prod_2023/prod_09_2023.csv",
        # "prod_2023/prod_10_2023.csv",
        # "prod_2023/prod_11_2023.csv",
        # "prod_2023/prod_12_2023.csv",
    ]

    df = preprocess_csv_data(data_files)

    df = df.fillna(0)
    return df
