import pandas as pd
from load_transactions import load_sofi, load_chase
from expense_summary import build_expense_summary
from income_summary import build_income_summary
from to_excel import write_excel
from functions import combine_joint_chase, normalize_output
from Categories import categories
from summary import run_summary

to_excel = True

from_date = '11/2025'
to_date = '11/2025'



all_periods = pd.date_range("2025-01-01", "2025-12-01", freq="MS").strftime("%m/%Y").tolist()
start, end = from_date, to_date
selected_periods = all_periods[all_periods.index(start): all_periods.index(end)+1]

print("Selected periods:", selected_periods)


chase_filename = 'chase'
sofi_filename = 'sofi'


def run_pipeline(chase_filename,sofi_filename):
    df_sofi = load_sofi(sofi_filename, periods = selected_periods,categories=categories)
    df_chase = load_chase(chase_filename, periods=selected_periods,categories=categories)
    outflows, alerts = build_expense_summary(df_sofi=df_sofi,df_chase=df_chase)
    inflows = build_income_summary(df_sofi,df_chase)
    combined_df = combine_joint_chase(df_chase=df_chase,df_joint=df_sofi)
    norm_outflows = normalize_output(outflows)
    summary = run_summary(df_outflows=outflows,df_inflows=inflows)

    if to_excel == True:
        write_excel(date=to_date,outflow_df=norm_outflows,inflow_df=inflows,combined_df=combined_df,summary_df=summary)
    else:
        print("to_excel is set to False")




if __name__ == "__main__":

   run_pipeline(chase_filename,sofi_filename)




