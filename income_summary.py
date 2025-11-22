import pandas as pd


def build_income_summary(df_sofi, df_chase):
    cc = df_chase
    checking = df_sofi

    # Credit card: expenses are negative; ignore payments & returns
    cc_income = cc[cc["Amount"] > 0]

    # Checking: expenses are negative; ignore deposits
    checking_income = checking[checking["Amount"] > 0]

    # Combine
    combined = pd.concat([
        cc_income[["Category", "Amount"]],
        checking_income[["Category", "Amount"]],
    ])
    summary = combined.groupby("Category")["Amount"].sum().abs()

    summary_income = summary.to_frame().reset_index()
    summary_income.columns = ["Category", "Amount"]





    return summary_income
