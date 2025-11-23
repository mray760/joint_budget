import pandas as pd


def combine_joint_chase(df_chase,df_joint):
    df_chase['Bank'] = 'Chase'
    df_joint['Bank'] = 'Sofi'
    df_chase.rename(columns = {'Post Date': 'Date'}, inplace=True)
    df_chase = df_chase[['Date', 'Description', 'Type','Amount', 'Category','Bank']]
    combined_df = pd.concat([df_joint,df_chase])
    return combined_df
