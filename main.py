import pandas as pd
from load_transactions import load_sofi, load_chase
from expense_summary import build_expense_summary
from income_summary import build_income_summary
from to_excel import write_excel
from functions import combine_joint_chase
from Categories import categories

to_excel = True

from_date = '11/2025'
to_date = '11/2025'



all_periods = pd.date_range("2025-01-01", "2025-12-01", freq="MS").strftime("%m/%Y").tolist()
start, end = from_date, to_date
selected_periods = all_periods[all_periods.index(start): all_periods.index(end)+1]

print("Selected periods:", selected_periods)


chase_filename = 'chase_test'
sofi_filename = 'sofi_test'


def run_pipeline(chase_filename,sofi_filename):
    df_sofi = load_sofi(sofi_filename, periods = selected_periods,categories=categories)
    df_chase = load_chase(chase_filename, periods=selected_periods,categories=categories)
    summary_expense, alerts = build_expense_summary(df_sofi=df_sofi,df_chase=df_chase)
    summary_income = build_income_summary(df_sofi,df_chase)
    combined_df = combine_joint_chase(df_chase=df_chase,df_joint=df_sofi)
    if to_excel == True:
        write_excel(date=to_date,expense_df=summary_expense,income_df=summary_income,combined_df=combined_df)
    else:
        print("to_excel is set to False")
    return summary_expense, alerts , summary_income



if __name__ == "__main__":

    summary_expense, alerts, summary_income = run_pipeline(chase_filename,sofi_filename)




