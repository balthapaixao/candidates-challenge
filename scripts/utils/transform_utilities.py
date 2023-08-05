# Transform
def rename_columns(columns: list) -> list:
    return [col.replace(" ", "_") for col in columns]


def treat_dates(df: pd.DataFrame, date_cols: list) -> pd.DataFrame:
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col])
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    # renaming columns
    columns = df.columns
    df.columns = rename_columns(columns=columns)

    # Treating dates
    date_cols = ["Application_Date"]
    df = treat_dates(df=df, date_cols=date_cols)

    return df
