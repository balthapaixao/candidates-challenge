import matplotlib.pyplot as plt
import seaborn as sns
from .crud_utilities import read_from_postgres


def plot_hires_per_tech():
    query_hires_per_tech = """
SELECT 
    TECHNOLOGY
    , COUNT(*) as hires
FROM 
    COMPANY.CANDIDATES.SCORES
WHERE 
    ((CODE_CHALLENGE_SCORE >= 7) 
    AND TECHNICAL_INTERVIEW_SCORE >= 7)
GROUP BY 
    TECHNOLOGY"""

    df_hires_per_tech = read_from_postgres(query_hires_per_tech)
    sns.set()
    plt.figure(figsize=(10, 10))

    plt.pie(
        df_hires_per_tech["hires"],
        labels=df_hires_per_tech["technology"],
        autopct="%1.1f%%",
    )
    plt.title("Hires per Technology")
    plt.savefig("../../data/plots/hires_per_tech.png")


def hires_per_year():
    query_hires_per_year = """
SELECT 
    EXTRACT(YEAR FROM APPLICATION_DATE) AS YEAR
    , COUNT(*) AS hires
FROM 
    COMPANY.CANDIDATES.SCORES
WHERE 
    ((CODE_CHALLENGE_SCORE >= 7) 
    AND TECHNICAL_INTERVIEW_SCORE >= 7)
GROUP BY
    EXTRACT(YEAR FROM APPLICATION_DATE)
ORDER BY
    YEAR"""

    df_hires_per_year = read_from_postgres(query_hires_per_year)
    years = [str(int(year)) for year in df_hires_per_year["year"]]
    hires = df_hires_per_year["hires"].to_list()

    for index, value in enumerate(hires):
        plt.text(value, index, str(value), va="center")

    plt.barh(years, hires, color="r", edgecolor="black")
    plt.title("Hires per Year")
    plt.ylabel("years")
    plt.xlabel("hires")
    plt.savefig("../../data/plots/hires_per_year.png")


def hires_per_seniority():
    query_hires_per_seniority = """
SELECT
    SENIORITY
    , COUNT(*) AS hires
FROM
    COMPANY.CANDIDATES.CHALLENGE_SCORES
WHERE
    ((CODE_CHALLENGE_SCORE >= 7)
    AND TECHNICAL_INTERVIEW_SCORE >= 7)
GROUP BY
    SENIORITY
"""
    df_hires_per_seniority = read_from_postgres(query_hires_per_seniority)
    seniority = df_hires_per_seniority["seniority"].to_list()
    hires = df_hires_per_seniority["hires"].to_list()

    for index, value in enumerate(hires):
        plt.text(index, value, str(value), ha="center", va="bottom")

    plt.bar(seniority, hires, color="r", edgecolor="black")
    plt.title("Hires by Seniority")
    plt.ylabel("Seniority")
    plt.xlabel("hires")
    plt.savefig("../../data/plots/hires_per_seniority.png")


def hires_per_country():
    query_hires_per_country = """
SELECT 
    COUNTRY
    , EXTRACT(YEAR FROM APPLICATION_DATE) AS YEARS
    , COUNT(*) AS hires
FROM 
    COMPANY.CANDIDATES.SCORES
WHERE
    ((CODE_CHALLENGE_SCORE >= 7) 
    AND (TECHNICAL_INTERVIEW_SCORE >= 7) 
    AND COUNTRY IN ('United States of America', 'Brazil', 'Colombia', 'Ecuador'))
GROUP BY
    COUNTRY
    , EXTRACT(YEAR FROM APPLICATION_DATE)
ORDER BY
    YEARS
    , COUNTRY
"""
    df_hires_per_country = read_from_postgres(query_hires_per_country)

    plt.figure(figsize=(12, 6))

    df_hires_per_country["years"] = pd.to_numeric(
        df_hires_per_country["years"], downcast="integer"
    )

    sns.lineplot(data=df_hires_per_country, x="years", y="hires", hue="country")
    # display quantity centered per year
    for index, row in df_hires_per_country.iterrows():
        plt.text(
            row["years"], row["hires"], str(row["hires"]), ha="center", va="bottom"
        )

    plt.title("Hires over years")
    plt.savefig("../../data/plots/hires_per_country.png")
