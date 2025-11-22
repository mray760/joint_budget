import pandas as pd
from load_transactions import load_sofi, load_chase
from expense_summary import build_expense_summary
from income_summary import build_income_summary
from to_excel import write_excel

to_excel = True

date = '11.2025'
chase_filename = 'chase_test'
sofi_filename = 'sofi_test'


def run_pipeline(chase_filename,sofi_filename):
    df_sofi = load_sofi(sofi_filename)
    df_chase = load_chase(chase_filename)
    summary_expense, alerts = build_expense_summary(df_sofi=df_sofi,df_chase=df_chase)
    summary_income = build_income_summary(df_sofi,df_chase)
    if to_excel == True:
        write_excel(date=date,expense_df=summary_expense,income_df=summary_income,df_sofi=df_sofi,df_chase=df_chase)
    else:
        print("to_excel is set to False")
    return summary_expense, alerts , summary_income



if __name__ == "__main__":

    summary_expense, alerts, summary_income = run_pipeline(chase_filename,sofi_filename)



    print("\n===== Spending Summary =====")
    print(summary_expense)

    print("\n===== Budget Alerts =====")
    if alerts:
        for a in alerts:
            print(a)
    else:
        print("All categories are within budget ✔️")


    print(summary_income)

