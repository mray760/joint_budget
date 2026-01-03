import pandas as pd

def build_expense_summary(combined_transactions,expense_cat,investment_cat):
    
    # Credit card: expenses are negative; ignore payments & returns
    combined_transactions = combined_transactions[combined_transactions["Amount"] < 0]


    summary = combined_transactions.groupby("Category")["Amount"].sum()


    summary_expense = summary.to_frame().reset_index()
    summary_expense.columns = ["Category", "Amount"]

    df = summary_expense

    if (~df['Category'].isin(expense_cat + investment_cat)).any():
        print("Unknown expense category")


    df["Type"] = df["Category"].apply(
        lambda x: "Expense" if x in expense_cat
        else ("Investment" if x in investment_cat else None)
    )

    df = df[['Type', 'Category', 'Amount']]

    # Split into two groups
    expense_df = df[df['Type'] == 'Expense'].copy()
    investment_df = df[df['Type'] == 'Investment'].copy()

    # Create section headers
    expense_header = pd.DataFrame({'Type': ['Expense'], 'Category': [''], 'Amount': ['']})
    investment_header = pd.DataFrame({'Type': ['Investment'], 'Category': [''], 'Amount': ['']})

    # Blank spacer rows
    blank_rows = pd.DataFrame({'Type': [''], 'Category': [''], 'Amount': ['']})
    blank_rows2 = blank_rows.copy()

    # Build final output
    final_df = pd.concat([
        expense_header,
        expense_df.assign(Type=""),  # remove repeated labels
        blank_rows,
        investment_header,
        investment_df.assign(Type=""),  # remove repeated labels
    ], ignore_index=True)

    return final_df


