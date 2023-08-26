from utils.transform_utilities import transform
from utils.crud_utilities import insert_postgres
from utils.plot_utilities import main_plots
import pandas as pd


def main():
    df = pd.read_csv("./data/candidates.csv", sep=";")
    df_t = transform(df=df)

    insert_postgres(df=df_t, table_name="HIRE_CO_INC.CANDIDATES.CHALLENGE_SCORES")

    main_plots()


if __name__ == "__main__":
    main()
