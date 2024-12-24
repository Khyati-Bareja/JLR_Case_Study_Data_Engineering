# Data Preprocessing
import re
import pandas as pd
import logging
from config import path4

log_filename = path4
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')
# Basic null checks
def check_null_values(df, df_name):
    null_counts = df.isnull().sum()
    null_summary = f"Null values in {df_name}:\n{null_counts}"
    logging.info(null_summary)
    return 0   

# Deduplication of the base_data based on VIN, Option's Code, Model_Text and Sales Price
def check_option_code_duplicates(base_dataDF):
    base_dataDF = base_dataDF.drop_duplicates(subset=['VIN','Options_Code', 'Model_Text', 'Sales_Price'], keep='first')
    
    duplicates_summary = {}
        # Check duplicates for each unique option code
    for option_code in base_dataDF['Options_Code'].unique():
        # then i filter this for each option code
        filtered_data = base_dataDF[base_dataDF['Options_Code'] == option_code]
        # here i check for duplicates within the filtered data
        option_duplicates = filtered_data[filtered_data.duplicated(subset=['VIN', 'Options_Code', 'Model_Text', 'Sales_Price'], keep=False)]
        # if duplicates exist, adding them to the summary
        if not option_duplicates.empty:
            duplicates_summary[option_code] = option_duplicates
        else:
            duplicates_summary[option_code] = "No duplicates found"
        # and i log the duplicates summary
        if duplicates_summary:
            logging.info(f"Duplicates Summary: {duplicates_summary}")
        else:
            logging.info("No duplicates found after cleaning the data.")

    return base_dataDF

# Transformation1:  Extracting model code in base_data's Model_Text field 
def clean_model_text(value_in):
    value = str(value_in)
    if pd.isna(value):
        return value
    elif '/' in value:
        code = value.split('/')[0].strip()
        val = code.split()[0]
        if re.match('^[A-Z][0-9]{3}$', val):  
            return val
        else:
            return "Invalid"
    else:
        return value.split()[0] 

    
def baseData_update_modelText(base_dataDF):
    base_dataDF.loc[:, 'Model_Text'] = base_dataDF['Model_Text'].apply(clean_model_text)
    logging.info("Model_Text has been cleaned successfully.")
    return base_dataDF 

# Transformation 2: drop column: Options_desc not needed and with large number of null values 
def drop_column(base_dataDF):
    updated_baseDF = base_dataDF.drop('Option_Desc',axis = 1)
    logging.info("Options Description column dropped successfully: dropping due to high number of null values.")
    return updated_baseDF



# Checks the accuracy of Sales Price and Material Cost in Base Data and Options Data.

def check_data_accuracy(base_dataDF, options_dataDF):
    
    zero_or_negative_sales_pc = base_dataDF[base_dataDF['Sales_Price'] <= 0]  
    invalid_sales_pc = base_dataDF[base_dataDF['Sales_Price'].isnull()] 
    zero_or_negative_material_cost = options_dataDF[options_dataDF['Material_Cost'] <= 0]
    invalid_material_cost = options_dataDF[options_dataDF['Material_Cost'].isnull()] 

    summary = {
        "invalid_sales_pc_count": len(invalid_sales_pc),
        "zero_or_negative_sales_pc_count": len(zero_or_negative_sales_pc),
        "invalid_material_cost_count": len(invalid_material_cost),
        "zero_or_negative_material_cost_count": len(zero_or_negative_material_cost)
    }
    logging.info(f"Data Accuracy Summary: {summary}")
    return 0



#Cross-field Validation check for data consistency: Comparing Model_text column of Base_data with valid Model codes for comparison with Model Codes in Options_data
# and nameplate_code in vehicle_line_mapping. 
def cross_field_validation(base_dataDF, options_dataDF, vehicle_line_mappingDF):
    # Extract unique values for model codes and option codes
    base_models = base_dataDF['Model_Text'].unique()
    option_models = options_dataDF['Model'].unique()
    vehicle_line_mapping_models = vehicle_line_mappingDF['nameplate_code'].unique()
    base_option_code = base_dataDF['Options_Code'].unique()
    options_data_option_code = options_dataDF['Option_Code'].unique()

    validation_summary = {
        "models unique to base data file": print(set(base_models) - set(option_models)),
        "models unique to options data file": print(set(option_models) - set(base_models)),
        "\n common_models_base_vehicle_line": print(set(vehicle_line_mapping_models).intersection(set(base_models))),
        "\n common_models_option_vehicle_line": set(vehicle_line_mapping_models).intersection(set(option_models)),
        "\n option codes unique to base data file": set(base_option_code) - set(options_data_option_code),
        "\n option codes unique to options data file": set(options_data_option_code) - set(base_option_code)
    }
    logging.info(f"Cross-field Validation Summary: {validation_summary}")
    return 0


