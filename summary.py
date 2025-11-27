import pandas as pd

def run_summary(df_outflows,df_inflows):

    # -------------------------
    # 1. STARTING DATAFRAMES
    # -------------------------
    # df_outflows (Type, Category, Amount)
    # df_inflows (Category, Amount)


    # -------------------------
    # 2. SPLIT OUT INVESTMENTS CLEANLY
    # -------------------------
    # Extract investments from BOTH inflows & outflows
    investing_df = pd.concat([
        df_outflows[df_outflows["Category"] == "Investments"],
        df_inflows[df_inflows["Category"] == "Investments"]
    ], ignore_index=True)

    # Remove them from inflows & outflows
    df_outflows_clean = df_outflows[df_outflows["Category"] != "Investments"].copy()
    df_inflows_clean = df_inflows[df_inflows["Category"] != "Investments"].copy()

    df_outflows_clean['Amount'] = pd.to_numeric(df_outflows_clean['Amount'], errors='coerce')
    df_inflows_clean['Amount'] = pd.to_numeric(df_inflows_clean['Amount'], errors='coerce')
    investing_df['Amount'] = pd.to_numeric(investing_df['Amount'], errors='coerce')

    # -------------------------
    # 3. CALCULATE TOTALS (STRICTLY USING CLEAN DFS)
    # -------------------------
    total_outflows = df_outflows_clean['Amount'].sum()     # no investments
    total_inflows  = df_inflows_clean['Amount'].sum()      # no investments
    total_investing = investing_df['Amount'].sum()         # only investments


    # Outflows are negative, so leftover = inflows + outflows + investing
    left_over = total_inflows + total_outflows + total_investing


    # -------------------------
    # 4. BUILD SUMMARY TABLE
    # -------------------------
    summary = pd.DataFrame({
        "Description": [
            "Total Inflows",
            "Total Outflows",
            "Total Investing",
            "Left Over"
        ],
        "Amount": [
            round(total_inflows, 2),
            round(total_outflows, 2),
            round(total_investing, 2),
            round(left_over, 2)
        ]
    })

    #summary['Amount'] = summary['Amount'].map("{:,.2f}".format)



    # -------------------------
    # 5. ASSEMBLE FINAL REPORT
    # -------------------------
    header_inflows = pd.DataFrame({"Description": ["INFLOWS"], "Amount": [""]})
    header_outflows = pd.DataFrame({"Description": ["OUTFLOWS"], "Amount": [""]})
    header_investing = pd.DataFrame({"Description": ["INVESTING"], "Amount": [""]})
    summary_header = pd.DataFrame({"Description": ["SUMMARY"], "Amount": [""]})
    blank = pd.DataFrame({"Description": [""], "Amount": [""]})

    report = pd.concat([
        header_inflows,
        df_inflows_clean.rename(columns={"Category": "Description"}),
        blank,

        header_outflows,
        df_outflows_clean[['Category', 'Amount']].rename(columns={"Category": "Description"}),
        blank,

        header_investing,
        investing_df[['Category', 'Amount']].rename(columns={"Category": "Description"}),
        blank,

        summary_header,
        summary
    ], ignore_index=True)

    # Nicely format numbers
    #report["Amount"] = report["Amount"].replace("", None)
    #report["Amount"] = report["Amount"].apply(
        #lambda x: "{:,.2f}".format(x) if isinstance(x, (int, float)) else x
    #)



    return report
