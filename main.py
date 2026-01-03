import pandas as pd



from data_intake.load_transactions import load_sofi, load_chase
from reporting.income_summary import build_income_summary
from export.to_excel import write_excel
from normalization.functions import combine_joint_chase, run_periods_norm, create_categories
from normalization.post_di_norm import chase_norm,sofi_norm
from reporting.summary import run_summary
from reporting.expense_summary import build_expense_summary
from scratch import build_expense_summary


to_excel = False

from_date = '12/2025'
to_date = '12/2025'

chase_filename = 'chase'
sofi_filename = 'sofi'



def run_pipeline(chase_filename,sofi_filename):
    selected_periods = run_periods_norm(to_date=to_date,from_date=from_date)
    all_categories,expense_categories,income_categories,investment_categories = create_categories()

    ## Data Intake
    sofi_raw = load_sofi(sofi_filename, periods = selected_periods,categories=all_categories)
    chase_raw = load_chase(chase_filename, periods=selected_periods,categories=all_categories)

    ##Normalization
    df_sofi_norm = sofi_norm(sofi_raw,categories=all_categories)
    df_chase_norm = chase_norm(chase_raw,categories=all_categories)
    combined_transactions = combine_joint_chase(df_chase=df_chase_norm,df_joint=df_sofi_norm)

    ##Reporting
    outflows = build_expense_summary(combined_transactions=combined_transactions,expense_cat=expense_categories,investment_cat=investment_categories)
    inflows = build_income_summary(combined_transactions=combined_transactions)
    summary = run_summary(df_outflows=outflows,df_inflows=inflows)

    if to_excel == True:
        write_excel(date=to_date,outflow_df=outflows,inflow_df=inflows,combined_df=combined_transactions,summary_df=summary)
    else:
        print("to_excel is set to False")




if __name__ == "__main__":

   run_pipeline(chase_filename,sofi_filename)




