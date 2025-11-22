import pandas as pd


thresholds = {
        "Groceries": 1300,
        "Gas": 500,
        "Food & Drink": 250,
        "Insurance": 95,
        "Utilities": 100,
        "Subscriptions": 400,
        "Entertainment": 75,
        "Other": 100,
        "Pet Food": 150
    }


def build_expense_summary(df_sofi,df_chase):
    cc = df_chase
    checking = df_sofi

    # Credit card: expenses are negative; ignore payments & returns
    cc_expenses = cc[cc["Amount"] < 0]

    # Checking: expenses are negative; ignore deposits
    checking_expenses = checking[checking["Amount"] < 0]

    # Combine
    combined = pd.concat([
        cc_expenses[["Category", "Amount"]],
        checking_expenses[["Category", "Amount"]],
    ])

    summary = combined.groupby("Category")["Amount"].sum()

    # Budget check
    alerts = []
    for cat, total in summary.items():
        if cat in thresholds and total > thresholds[cat]:
            alerts.append(f"⚠️ OVER BUDGET: {cat} – ${total:.2f} (limit ${thresholds[cat]:.2f})")

    summary_expense = summary.to_frame().reset_index()
    summary_expense.columns = ["Category", "Amount"]

    return summary_expense, alerts
