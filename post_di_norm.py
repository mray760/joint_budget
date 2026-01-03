import pandas as pd


##### Chase

def chase_norm(raw_chase,categories):
    df = raw_chase[["Transaction Date", "Post Date", "Description",
        "Category", "Type", "Amount"]]
    
    df = df[~df['Type'].str.contains('Payment',case = False, na=False) ]

    df.loc[df["Description"].str.contains("Kindle Svcs", na=False), "Category"] = "Subscriptions"
    df.loc[df["Description"].str.contains("PETCO", na=False), "Category"] = "Pet Food"
    df.loc[df["Description"].str.contains("FITNESS LEGENDZ", na=False), "Category"] = "Subscriptions"
    df.loc[df["Description"].str.contains("KALSHI", na=False), "Category"] = "Leisure"
    df.loc[df["Description"].str.contains("JD`S BODEGA", na=False), "Category"] = "Leisure"
    df.loc[df["Description"].str.contains("BARBER STORY", na=False), "Category"] = "Subscriptions"

    

    df = df[~df["Description"].str.contains("Zelle payment from Matt Ray", case=False, na=False)]
    df = df[~df["Description"].str.contains("Payment Thank You - Web", case=False, na=False)]


    df["Category"] = df["Category"].replace({
        "Food & Drink": "Leisure",
        "Shopping": "Leisure",
        "Health & Wellness": "Leisure",
        "Entertainment": "Leisure",
        "Bills & Utilities": "Utilities",
        "Travel": "Leisure"
    })
    df["Category"] = df["Category"].str.strip()

    bad = df[~df["Category"].isin(categories)]
    print("Rows NOT in categories list:")
    print(bad[["Description", "Category"]].head(20))

    mask = ~df["Category"].isin(categories)

    df.loc[mask & (df["Amount"] > 0), "Category"] = "Other Income"
    df.loc[mask & (df["Amount"] < 0), "Category"] = "Other Expense"

    return df




##### SOFI

CHECKING_CATEGORY_MAP = {
    "STATE FARM": "Insurance",
    "IDAHO POWER": "Utilities",
    "INTERMOUNTAIN": "Utilities",
    "COVENANT": "Subscriptions",
    "CHATGPT": "Subscriptions",
    "Spotify": "Subscriptions",
    "TACO": "Leisure",
    "TRADER": "Groceries",
    "Zelle¬Æ Payment to Amy Ray": "Amys Allowance",
    "Zelle® Payment to Amy Ray": "Amys Allowance",
    "FITNESS LEGENDZ": "Subscriptions",
    "PETCO": "Pet Food",
    "NSM DBAMR.COOPER": "Mortgage",
    "ST LUKE'S HS": "Direct Deposit - Amy",
    "Clearwater A-OSV" : "Direct Deposit - Matt",
    "Zelle¬Æ Payment to Amy Bellenbaum": "Amys Allowance",
    "RENT": "Rent",
    "Rent": "Rent",
    "MSPBNA": "Investments",
    "COINBASE": 'Investments',
    "Coinbase": "Investments",
    "VERIZON" : "Subscriptions",
    "VZWRLSS" : "Subscriptions"
}



def sofi_norm(sofi_raw,categories):
    df = sofi_raw[["Date", "Description", "Type", "Amount"]]
    df = df[~df["Description"].str.contains("CHASE CREDIT CRD", case=False, na=False)]
    df = df[~df["Description"].str.contains("Zelle¬Æ Payment from Amy Ray", case=False, na=False)]
    df = df[~df["Description"].str.contains("Payment Thank You - Web", case=False, na=False)]
    df = df[~df["Description"].str.contains("Payment Thank You - Web", case=False, na=False)]


    def map_checking_category(row):
        desc = row["Description"]
        amount = row["Amount"]

        # First: check category mappings
        for k, v in CHECKING_CATEGORY_MAP.items():
            if k.upper() in desc.upper():
                return v

        # Otherwise: classify based on amount
        if amount > 0:
            return "Other Income"
        else:
            return "Other Expense"


    df.loc[
        (df["Description"] == "VENMO") & (df["Amount"] > 0),
        "Category"
    ] = "Venmo Income"
    df.loc[
        (df["Description"] == "VENMO") & (df["Amount"] < 0),
        "Category"
    ] = "Venmo Expense"
    df.loc[
        (df["Description"].str.contains("Zelle")) & (df["Amount"] > 0) & (~df["Description"].str.contains("payment to amy ray", case=False, na=False)),
        "Category"
    ] = "Zelle Income"
    df.loc[
        (df["Description"].str.contains("Zelle")) & (df["Amount"] < 0) & (~df["Description"].str.contains("payment to amy ray", case=False, na=False)),
        "Category"
    ] = "Zelle Expense"
    df["Category"] = df.apply(map_checking_category, axis=1)

    mask = ~df["Category"].isin(categories)

    df.loc[mask & (df["Amount"] > 0), "Category"] = "Other Income"
    df.loc[mask & (df["Amount"] < 0), "Category"] = "Other Expense"

    return df

