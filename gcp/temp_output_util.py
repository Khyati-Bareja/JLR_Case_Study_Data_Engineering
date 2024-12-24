import datetime

#This function generates a unique filename each time it’s called by appending a timestamp to a fixed prefix
def get_output_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") #formating date and time to string
    return f"tempoutput_{timestamp}.txt"

def write_to_temp_file(content):
    filename = get_output_filename() # calling above func, to get unique filename for curr run
    with open(filename, "a") as f:  #opening the file in append mode ("a"), though not needed 
        f.write(content)            # but will ensure that a file of the same name exists, it will not overrite the exisiting one
    return filename