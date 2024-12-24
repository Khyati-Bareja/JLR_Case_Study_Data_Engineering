from google.cloud import storage

def check_if_files_exist(bucket_name,csv_files):
    client = storage.Client.from_service_account_json("/Users/khyati/Documents/Resumes/JLR/111385 - DataEngineer CaseStudy/vehiclesproject-001-1227199fdaa1.json")   # Initialze the storage client
    bucket = client.get_bucket(bucket_name) # Fetching the bucket
    for file_name in csv_files:
        blob = bucket.blob(file_name)
        if blob.exists():
            print("file with name: ",{file_name}," exist.")
        else:
            print("file with name: ",{file_name}," missing.")

bucket_name = "raw_data_vehicles_bucket"
csv_files = ['base_data.csv','options_data.csv','vehicle_line_mapping.csv']
check_if_files_exist(bucket_name, csv_files)



