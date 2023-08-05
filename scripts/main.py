from .utils.transform_utilities import transform
from .utils.crud_utilities import insert_into_table
import pandas as pd


def main():
    df = pd.read_csv("../data/candidates.csv", sep=";")
    df_t = transform(df=df)

    insert_into_table(df=df_t, table_name="candidates")


if __name__ == "__main__":
    main()
