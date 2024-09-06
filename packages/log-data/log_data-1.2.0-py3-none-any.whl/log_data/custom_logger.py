from psycopg2 import OperationalError,Error
import os
import psycopg2
import inspect
import subprocess
from datetime import datetime

# from .notion import *
from custom_development_standardisation import *
from .utility import *


class custom_logger():
    def __init__(self):
        print("HELLO THERE")
        # print("Generating logger....")
        self.logging_in_progress = False
        
        self.storage_location = "database"
        # self.notion_log_page_id = ''
        # self.notion_headers = {
        #     'Authorization': f'Bearer {os.environ['api_key']}',
        #     'Content-Type': 'application/json',
        #     'Notion-Version': '2022-06-28'
        # }
        # self.backup_notion_page_id = "b74cbfbe7cc2490e9dc3210f06eb3c8e"
        self.logging_table_name = os.environ['database_table']
        self.logging_table_columns = None
        self.connection = None
        self.client = None
    
    def change_storage_location(self):
        if self.storage_location == "log":
            self.storage_location = "database"
        if self.storage_location == "database":
            self.storage_location = "log"

    def test_notion_connection(self):
        outcome = get_page(self.backup_notion_page_id)
        if outcome["outcome"] == "error":
            return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
        return generate_outcome_message("success",outcome["output"])

    def initialise_database(self):
        
        user = os.environ["database_user"]
        host = os.environ["database_host"]
        port = os.environ["database_port"]
        database_name = os.environ['database_name']
        table_name = os.environ['database_table']
        password = os.environ['password']
        
        try:
            
            self.connection = psycopg2.connect(
                database=database_name,
                user=user,
                host=host,
                port=port,
                password=password
            )
            self.client = self.connection.cursor()
            
            # 👀 Check if table exist
            self.client.execute("""SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');""")
            outcome = self.client.fetchall()
            reformatted = [item[0] for item in outcome]
            exist = False
            for i in reformatted:
                if i == table_name:
                    exist = True
                    break
            if exist == False:
                return generate_outcome_message(f"{table_name} does not exist in database {database_name}...")
            
            
            # 🏃🏼‍♀️ GET COLUMNS FROM TABLE
            self.client.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
            outcome = self.client.fetchall()
            reformatted = []
            for i in outcome:
                name = i[0]
                # Remove id from the list
                if name != "id" and name != "timestamp":
                    reformatted.append(name)
                # Move time stamp to the first item in the list
            self.logging_table_columns = reformatted
            return generate_outcome_message("success",f"database reached. Primary storage location is {self.storage_location}...")
        
        except OperationalError as e:
            '''COMING SOON...Saving to a file locally...'''
            self.storage_location = "log"
            return generate_outcome_message("success","identified log as storage location")


    def get_logs(self):
        # Get the home directory
        home_directory = os.path.expanduser('~')
        
        # Define the file path for the .log file
        dotlog_file_path = os.path.join(home_directory, '.log')
        
        # Check if the .log file exists
        if not os.path.isfile(dotlog_file_path):
            return generate_outcome_message("error","No logs")
        
        with open(dotlog_file_path, 'r') as file:
            content = file.read()
            return content
        
    
    def get_date_time(self):
        current_datetime = datetime.now().replace(microsecond=0)
        return current_datetime
    

    def store_log(self):
        # get base package information (package name, file name, function name)
        
        x = inspect.stack()
        file_path = x[1].filename
        file_name = file_path.split("/")[-1]

        # Must be placed inside a function
        outcome = get_package_name(file_path)
        if outcome["outcome"] == "error":
            raise RuntimeError(f"\n\n Failed to get package name...\n\n{outcome['output']['message']}")
        package_name = outcome["output"]
        function_name = x[1].function
        
        stringing = f"{file_name},{package_name},{function_name}"
        
        if self.storage_location == "log":
            self.store_log_in_log_file(stringing)
            return generate_outcome_message("success",f"log message stored...")
        
        
        if self.storage_location == "database":
            outcome = self.store_log_in_database(stringing)

        # Log data is not properly set (generate error and stop all operation. Code is wrong)
        if outcome["outcome"] == "error" and outcome["output"]["status"] == False:                                                              
            self.logging_in_progress = False
            raise RuntimeError(f"\n\n something wrong with log data itself...\n\n{outcome['output']['message']}")
        
        # Something wrong with database connection (store data in log file)
        if outcome["outcome"] == "error" and outcome["output"]["status"] == True:
            self.store_log_in_log_file(stringing)

        return generate_outcome_message("success",f"log message stored...")

    def store_bulk_log_in_database(self):
        # Check if database can be connected again
        outcome = self.initialise_database()
        if outcome["output"] == "identified log as storage location":
            return generate_outcome_message("error","database not connected...",the_type="custom")
        
        
        # check if there is logs to store
        data = self.get_logs()
        if data["outcome"] == "error":
            return generate_outcome_message("error","no logs to store",the_type="custom")

        # Generate the storing command
        with open('.log', 'r') as file:
            content = file.read()
        lines_array = content.split('\n')
        formatted_string = ', '.join(f'({item})' for item in lines_array if item)

        # Execute storing command
        try:
            self.client.execute(f"insert into {os.environ['database_table']} ({self.logging_table_columns}) values {formatted_string}")
            self.connection.commit()
            # Get the root directory path with .log file
            home_directory = os.path.expanduser('~')
            dotlog_file_path = os.path.join(home_directory, '.log')
            os.remove(dotlog_file_path)
            return generate_outcome_message("success","Logs stored in database")
        except psycopg2.Error as e:
            return generate_outcome_message("error",f"something went wrong with storing...: {e.message}")

        # Check if bulk

    # What if during the process, something went wrong? Store it in notion. 
    def store_log_in_database(self,log_data):
            # CHECK LOG DATA TO SEE IF IT IS READY FOR STORAGE
            if isinstance(log_data,str) == False:
                return generate_outcome_message("error",{"status": False,"message": f"log_data parameter is not of type string..."},the_type="custom")
            splitted = log_data.split(",")
            table_column_number = len(self.logging_table_columns)
            data_length = len(splitted)
            # Check if the column length (exclude id and timestamp) is the same as the number of data specified
            if table_column_number != data_length:
                return generate_outcome_message("error",{"status": False,"message": f"Column number {table_column_number} is not the same as data length {data_length}..."},the_type="custom")

            # CHECK IF DATABASE IS REACHABLE
            if self.client == None:
                return generate_outcome_message("error",{"status": True, "message": f"client is empty..."},the_type="custom")
            if self.logging_table_name == None:
                return generate_outcome_message("error",{"status": True, "message": f"logging table name not specified..."},the_type="custom")
            if self.logging_table_columns == None:
                return generate_outcome_message("error",{"status" : True, "message": f"logging table columns for {self.logging_table_name} not specified..."},the_type="custom")
            
            # Construct the column name portion of the insert command (ADD timestamp column)
            stringing_columns = 'timestamp,'+",".join(self.logging_table_columns)
            
            # Get current date time (seconds precision)
            current_date_time = datetime.now()
            formatted_time = current_date_time.strftime('%Y-%m-%d %H:%M:%S')
            formatted_time = datetime.strptime(formatted_time, '%Y-%m-%d %H:%M:%S')
            timestamper = formatted_time.timestamp()
            
            string_format = f"TO_TIMESTAMP({timestamper}),"
            for index,i in enumerate(splitted):
                string_format += f"'{i}'"
                if index != data_length - 1:
                    string_format += "," 
            
            command = f"insert into {self.logging_table_name} ({stringing_columns}) values ({string_format})"
            
            try:
                outcome = self.client.execute(command)
                self.connection.commit()
            except psycopg2.Error as e:
                return generate_outcome_message("error",{"status": True,"message": f"Something went wrong with execution..."},the_type="others")
            
            return generate_outcome_message("success","data logged...")
        # if self.storage_location == "notion":

    def store_log_in_log_file(self,log_data):
        current_date_time = datetime.now()
        formatted_time = current_date_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_time = datetime.strptime(formatted_time, '%Y-%m-%d %H:%M:%S')
        timestamper = formatted_time.timestamp()
        string_format = f"TO_TIMESTAMP({timestamper}),"
        store_data_in_file(string_format+","+log_data)
        

# # Local testing
# a = custom_logger()
# a.initialise_database("logging_data","usage_data")
# a.change_storage_location()
# def test():
#     print("lel:",a.store_log())
#     print("hello there.......")
# test()
