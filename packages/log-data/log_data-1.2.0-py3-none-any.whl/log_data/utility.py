import subprocess
from custom_development_standardisation import *
import re
import os

def get_package_name(path_to_package_module):
    result = subprocess.run("pip show pip", shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        outcome = result.stdout
        one = outcome.split("\n")
        splitted = one[7].split("\n")
        path = None
        for i in one:
            splitted = re.split(r'[ :]+', i)
            if splitted[0] == "Location":
                path = splitted[1]
        # compare path to package
        splitted_path_1 = path.split("/")
        splitted_path_2 = path_to_package_module.split("/")
        length1 = len(splitted_path_1)
        package_name = splitted_path_2[length1]
        return generate_outcome_message("success",package_name)
    else:
        return generate_outcome_message("error",result.stderr,the_type="others")
    

# print(get_package_name("/opt/homebrew/lib/python3.11/site-packages/testering/test.py"))


def store_data_in_file(data):
    # Get the home directory
    home_directory = os.path.expanduser('~')
    
    # Check if a file named .logs exists in the home directory
    file_location = os.path.join(home_directory, '.logs')
    if not os.path.isfile(file_location):
        # If the file doesn't exist, create it and add the data
        with open(file_location, 'w') as f:
            f.write(data + '\n')
    else:
        # If the file exists, append the data to a new line at the end of the file
        with open(file_location, 'a') as f:
            f.write(data + '\n')
    return True
    


# store_data_in_file("blabla")

# what am I looking for?
# file name, -> filename,split,last item
#     - Based on experiments, the file name is the directory where the file actually is, and not the file that executed it.
#     - Since I am logging packages, I need to know where the package is. 
#     - pip show pip can show that. 
# package name -> 