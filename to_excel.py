import pandas as pd

output_file = '/Users/mattray/Desktop/Budget/outputs'


def write_excel(date, expense_df, income_df,df_chase,df_sofi):

    output_path = fr'/Users/mattray/Desktop/Budget/outputs/{date}.xlsx'

    # Dictionary of sheets to write
    sheets = {
        "Expenses": expense_df,
        "Income": income_df,
        "Sofi - Normaliezd": df_sofi,
        "Chase - Normalized": df_chase
    }

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:

        # --- Create all sheets first ---
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # --- Now apply formatting ---
        workbook = writer.book
        money_fmt = workbook.add_format({'num_format': '#,##0.00'})
        text_fmt = workbook.add_format({'num_format': '@'})

        for sheet_name, df in sheets.items():

            worksheet = writer.sheets[sheet_name]

            for i, col in enumerate(df.columns):

                # Set column width
                try:
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                except Exception:
                    max_len = len(col) + 2

                # Apply numeric or text formatting
                if pd.api.types.is_numeric_dtype(df[col]):
                    worksheet.set_column(i, i, max_len, money_fmt)
                else:
                    worksheet.set_column(i, i, max_len, text_fmt)

    print(f"✅ Successfully saved Excel file: {output_path}")
