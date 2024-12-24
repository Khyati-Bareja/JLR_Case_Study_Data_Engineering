import main_run
import pandas as pd
from dataload import load_data_to_sql

updated_base_dataDF, options_dataDF, vehicle_line_mappingDF = main_run.main()

updated_base_dataDF['Production_Cost'] = 0
updated_base_dataDF['Profit'] = 0
def calculate_production_cost(row, options_df):
    sales_price = row['Sales_Price']
    model_text = row['Model_Text']
    options_code = row['Options_Code']
    #Case1
    if sales_price <= 0:
        return 0
    #Case2
    model_filtered = options_df[options_df['Model'] == model_text]
    exact_match = model_filtered[model_filtered['Option_Code'] == options_code]
    if not exact_match.empty:
        return exact_match['Material_Cost'].iloc[0]
    
    #Case3
    match2 = options_df[(options_df['Option_Code'] != options_code) & (options_df['Model'] == model_text)]
    if not match2.empty:
        avg_cost = match2['Material_Cost'].mean()
        if pd.notna(avg_cost):
            return avg_cost
    # Case4   
    else:
        cost = 0.45 * sales_price
        return cost
    # return 0

updated_base_dataDF['Production_Cost'] = updated_base_dataDF.apply(calculate_production_cost, args=(options_dataDF,), axis=1)
updated_base_dataDF['Profit'] = updated_base_dataDF['Sales_Price'] - updated_base_dataDF['Production_Cost']

print(updated_base_dataDF.head(50))

load_data_to_sql(updated_base_dataDF)