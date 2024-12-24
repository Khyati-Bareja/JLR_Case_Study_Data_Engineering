try:
    import os
    import io
    from io import BytesIO
    import pandas as pd
    from google.cloud import storage
except Exception as e:
    print("Issue Encountered, check for any missing modules {}".format(e))

storage_client = storage.Client.from_service_account_json("/Users/khyati/Documents/Resumes/JLR/111385 - DataEngineer CaseStudy/vehiclesproject-001-1227199fdaa1.json")

csv_file_paths = [
    "/Users/khyati/Documents/Resumes/JLR/111385 - DataEngineer CaseStudy/data_sets/base_data.csv",
    "/Users/khyati/Documents/Resumes/JLR/111385 - DataEngineer CaseStudy/data_sets/options_data.csv",
    "/Users/khyati/Documents/Resumes/JLR/111385 - DataEngineer CaseStudy/data_sets/vehicle_line_mapping.csv"]

def upload_to_gcs(bucket_name, csv_file_paths):
    # client = storage_client
    bucket = storage_client.get_bucket(bucket_name)

    for csv_file_path in csv_file_paths:
        blob = bucket.blob(os.path.basename(csv_file_path))
        blob.upload_from_filename(csv_file_path)
        
upload_to_gcs('raw_data_vehicles_bucket',csv_file_paths)
# print("data uploaded successfully!")

