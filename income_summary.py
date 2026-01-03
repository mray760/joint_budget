import pandas as pd


def build_income_summary(combined_transactions):
    df = combined_transactions

    df = df[df["Amount"]>0]

    summary = df.groupby("Category")["Amount"].sum().abs()

    summary_income = summary.to_frame().reset_index()
    summary_income.columns = ["Category", "Amount"]

    return summary_income
