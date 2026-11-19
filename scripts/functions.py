from itertools import combinations

import matplotlib.pyplot as plt
import pandas as pd
import pyodbc
import seaborn as sns
from scipy import stats
from scipy.stats import (
    bartlett,
    boxcox,
    f_oneway,
    fisher_exact,
    kruskal,
    mannwhitneyu,
    shapiro,
    ttest_ind,
)


def data_pull(query_sql_file):
    server = "ITAPPROREPP01"
    database = "UofC_DW_Student"

    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

    with open(query_sql_file, "r") as file:
        query = file.read()

    conn = pyodbc.connect(conn_str)

    df = pd.read_sql_query(sql=query, con=conn)

    return df


def test_names():
    TestName_dict = {
        "International English Language Testing System (IELTS)": "IELTS",
        "Test of English as a Foreign Language (TOEFL)": "TOEFL",
        "Duolingo": "Duolingo",
        "English for Academic Purposes (EAP)": "EAP",
        "No Test": "No Test",
        "Pearson Test of English (PTE)": "PTE",
    }

    return TestName_dict


def summarize(df, mainCol):
    summary_df = df.groupby(mainCol).agg(
        {
            "TestName": "count",
            "Cumulative_GPA": ["mean", "median"],
            "Discontinuation": ["sum", lambda x: (x == 1).mean() * 100],
        }
    )

    summary_df.columns = [
        "Test_Count",
        "Average_GPA",
        "Median_GPA",
        "Discontinuation",
        "Discontinuation_Rate",
    ]

    summary_df = summary_df.sort_values(by="Test_Count", ascending=False)

    return summary_df


def remove_outliers(df, column, k=1.5):
    # Calculate median and IQR
    median = df[column].median()
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    # Define lower and upper bounds for outliers
    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr

    # Filter DataFrame to remove outliers
    df_cleaned = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    return df_cleaned


def box_plot(df, numeric_column, categoric_column):
    sns.set(style="white")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x=categoric_column, y=numeric_column, ax=ax)
    ax.set_title(
        f"BoxPlot of {numeric_column} with respect to {categoric_column}",
        fontweight="bold",
    )
    ax.set_xlabel(categoric_column)
    ax.set_ylabel(numeric_column)
    plt.tight_layout()
    return fig


def get_qq_plot(df, numeric_column, categoric_column):
    fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(12, 6))

    for i, test_name in enumerate(df[categoric_column].unique()):
        data = df[df[categoric_column] == test_name][numeric_column]

        stats.probplot(data, dist="norm", plot=axs[i])
        axs[i].set_title(f"QQ Plot for {test_name}")
    plt.tight_layout()
    return fig


def get_density_plot(df, numeric_column, categoric_column):
    fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(12, 6))

    for i, test_name in enumerate(df[categoric_column].unique()):
        data = df[df[categoric_column] == test_name][numeric_column]

        sns.histplot(data, kde=True, ax=axs[i], stat="density")
        axs[i].set_title(f"Density Plot for {test_name}")

    plt.tight_layout()
    return fig


def check_normality(df, numeric_column, categoric_column, alpha):
    result = ""
    for test in df[categoric_column].unique():
        temp_df = df[df[categoric_column] == test]
        temp_data = temp_df[[numeric_column]]

        shapiro_stat, shapiro_p = shapiro(temp_data)
        check_normality = True

        if shapiro_p < alpha:
            result = result + f'- "{test}": p value = {shapiro_p:#.2f} - Not Normal\n'
            check_normality = False
        else:
            result = result + f'- "{test}": p value = {shapiro_p:#.2f} - Normal\n'
    return result, check_normality


def boxcox_tranformation(df, numeric_column):
    data = df[numeric_column]
    transformed_data, lambda_value = boxcox(data)
    col_name = numeric_column + "_Transformed"
    df[col_name] = transformed_data
    return df


def check_homoscedasticity(df, numeric_column, categoric_column, alpha):
    groups = []
    check_homoscedasticity = True
    for category in df[categoric_column].unique():
        groups.append(df[df[categoric_column] == category][numeric_column])

    stat, p_value = bartlett(*groups)

    if p_value < alpha:
        check_homoscedasticity = False
        result = f"Homoscedasticity Assumption: Failed (p_value: {p_value:#.2f})"
    else:
        result = f"Homoscedasticity Assumption: Passed (p_value: {p_value:#.2f})"

    return result, check_homoscedasticity


def kruskal_wallis_test(df, numeric_column, categoric_column, alpha):
    groups = []

    for category in df[categoric_column].unique():
        groups.append(df[df[categoric_column] == category][numeric_column])

    statistic, p_value = kruskal(*groups)

    if p_value < alpha:
        result = f"Reject the null hypothesis. At least one group has a different median. (p_value: {p_value:#.2f})"
    else:
        result = f"Fail to reject the null hypothesis. All groups have the same median. (p_value: {p_value:#.2f})"
    return result


def mann_whitney_test(df, numeric_column, categoric_column, alpha):
    result = ""
    for pair in combinations(df[categoric_column].unique(), 2):
        category1, category2 = pair

        data_category1 = df[df[categoric_column] == category1][numeric_column]
        data_category2 = df[df[categoric_column] == category2][numeric_column]

        statistic, p_value = mannwhitneyu(data_category1, data_category2)

        if p_value < alpha:
            result = (
                result
                + f"- {category1} vs. {category2}: Different medians (p_value = {p_value:#.2f})\n"
            )
        else:
            result = (
                result
                + f"- {category1} vs. {category2}: Equal medians (p_value = {p_value:#.2f})\n"
            )
    return result


def anova_test(df, numeric_column, categoric_column, alpha):
    groups = []

    for category in df[categoric_column].unique():
        groups.append(df[df[categoric_column] == category][numeric_column])

    statistic, p_value = f_oneway(*groups)

    if p_value < alpha:
        result = f"Reject the null hypothesis. At least one group has a different mean. (F: {statistic:#.2f}, p_value: {p_value:#.2f})"
    else:
        result = f"Fail to reject the null hypothesis. All groups have the same mean. (F: {statistic:#.2f}, p_value: {p_value:#.2f})"
    return result


def t_test_bonferroni(df, numeric_column, categoric_column, alpha):
    result = ""
    n_groups = len(df[categoric_column].unique())
    n_comparisons = n_groups * (n_groups - 1) / 2
    adjusted_alpha = alpha / n_comparisons

    for pair in combinations(df[categoric_column].unique(), 2):
        category1, category2 = pair

        data_category1 = df[df[categoric_column] == category1][numeric_column]
        data_category2 = df[df[categoric_column] == category2][numeric_column]

        _, p_value = ttest_ind(data_category1, data_category2)

        if p_value < adjusted_alpha:
            result += f"- {category1} vs. {category2}: Different means (p_value = {p_value:.4f}, adj_alpha = {adjusted_alpha:#.4f})\n"
        else:
            result += f"- {category1} vs. {category2}: Equal means (p_value = {p_value:.4f}, adj_alpha = {adjusted_alpha:#.4f})\n"

    return result


def bar_plot(df, numeric_column, categoric_column, y_lim=(0, 4), data_labels=False):
    ax = sns.barplot(
        data=df.sort_values(numeric_column), x=categoric_column, y=numeric_column
    )
    plt.xlabel(categoric_column)
    plt.ylabel(numeric_column)
    plt.title(f"{numeric_column} by {categoric_column}")
    plt.ylim(y_lim[0], y_lim[1])

    if data_labels:
        for i in ax.containers:
            ax.bar_label(
                i,
            )

    return ax.figure


def fisher_exact_test(summary_df, alpha, p_val_correction=True):
    summary_df["Cont."] = summary_df["Count"] - summary_df["Disc."]
    n_groups = len(summary_df["Test"].unique())
    n_comparisons = n_groups * (n_groups - 1) / 2
    adjusted_alpha = alpha / n_comparisons
    summary_df.set_index("Test", inplace=True)
    test_combinations = combinations(summary_df.index, 2)
    result = ""

    if p_val_correction:
        test_alpha = adjusted_alpha
    else:
        test_alpha = alpha

    for test1, test2 in test_combinations:
        contingency_table = summary_df.loc[[test1, test2], ["Disc.", "Cont."]].values
        _, p_value = fisher_exact(contingency_table)
        if p_value < test_alpha:
            result += f"- {test1} vs. {test2}: Different discontinuation rate (p_value = {p_value:.2f}, alpha = {test_alpha:#.4f})\n"
        else:
            result += f"- {test1} vs. {test2}: Equal discontinuation rate (p_value = {p_value:.2f}, alpha = {test_alpha:#.4f})\n"
    return result
