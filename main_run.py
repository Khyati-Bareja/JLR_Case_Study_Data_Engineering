# Main 

from dataingestion import load_data
from dataprocessing import ( check_null_values,check_option_code_duplicates, baseData_update_modelText, check_data_accuracy, drop_column, cross_field_validation)
from config  import path1, path2, path3
from dataload import load_data_to_sql


def main():

    base_dataDF = load_data(path1)
    options_dataDF = load_data(path2)
    vehicle_line_mappingDF = load_data(path3)

    # load_data_to_sql(base_dataDF)
    # load_data_to_sql(options_dataDF)
    # load_data_to_sql(vehicle_line_mappingDF)
    check_null_values(base_dataDF, 'Base Data')
    check_null_values(options_dataDF, 'Options Data')
    check_null_values(vehicle_line_mappingDF, 'Vehicle Line Mapping')   

    
    de_duplicated_base_data_df= check_option_code_duplicates(base_dataDF)

    updated_base_dataDF = baseData_update_modelText(de_duplicated_base_data_df)
    check_data_accuracy(updated_base_dataDF, options_dataDF)

    updated_base_dataDF = drop_column(updated_base_dataDF)
    # print(updated_base_dataDF.head(10))
    check_null_values(updated_base_dataDF, 'Base Data')
    # print(options_dataDF.head(10))
    # print(vehicle_line_mappingDF.head(10))
    cross_field_validation(updated_base_dataDF, options_dataDF, vehicle_line_mappingDF)

    return  updated_base_dataDF, options_dataDF, vehicle_line_mappingDF

if __name__ == "__main__":
    main()

