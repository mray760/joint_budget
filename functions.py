import pandas as pd
import json


def combine_joint_chase(df_chase,df_joint):
    df_chase['Bank'] = 'Chase'
    df_joint['Bank'] = 'Sofi'
    df_chase.rename(columns = {'Post Date': 'Date'}, inplace=True)
    df_chase = df_chase[['Date', 'Description', 'Type','Amount', 'Category','Bank']]
    combined_df = pd.concat([df_joint,df_chase])
    return combined_df



def run_periods_norm(from_date,to_date):
    all_periods = pd.date_range("2025-01-01", "2025-12-01", freq="MS").strftime("%m/%Y").tolist()
    start, end = from_date, to_date
    selected_periods = all_periods[all_periods.index(start): all_periods.index(end)+1]

    print("Selected periods:", selected_periods)

    return selected_periods


def create_categories():
    with open("classifications/categories.json") as f:
        json_data = json.load(f)
        all_categories = json_data['income'] + json_data['expense'] + json_data['investments']
        expense_categories = json_data['expense']
        income_categories = json_data['income']
        investment_categories = json_data['investments']

    return all_categories,expense_categories,income_categories,investment_categories
