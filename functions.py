import pandas as pd
from Categories import expense_cat, investment_cat


def combine_joint_chase(df_chase,df_joint):
    df_chase['Bank'] = 'Chase'
    df_joint['Bank'] = 'Sofi'
    df_chase.rename(columns = {'Post Date': 'Date'}, inplace=True)
    df_chase = df_chase[['Date', 'Description', 'Type','Amount', 'Category','Bank']]
    combined_df = pd.concat([df_joint,df_chase])
    return combined_df


def normalize_output(outflows):
    df = outflows

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

    final_df

    return final_df
