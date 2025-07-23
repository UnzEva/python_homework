import csv
import sys
import os
import custom_module
from datetime import datetime

# Task 2
#-----------------------------------------------------------------
def read_employees():
    employees_dict = {}
    rows_list = []

    try:
        with open('../csv/employees.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            employees_dict['fields'] = headers

            for row in reader:
                rows_list.append(row)

            employees_dict['rows'] = rows_list

    except FileNotFoundError:
        print("Error: The file '../csv/employees.csv' was not found.", file=sys.stderr)
        sys.exit(1)
    except csv.Error as e:
        print(f"CSV parsing error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    return employees_dict

employees = read_employees()

# Task 3
#---------------------------------------------------------------
def column_index(column_name):
    return employees["fields"].index(column_name)

employee_id_column = column_index("employee_id")

# Task 4
#---------------------------------------------------------------
def first_name(row_number):
    first_name_col = column_index("first_name")
    return employees["rows"][row_number][first_name_col]

# Task 5
#---------------------------------------------------------------
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    return list(filter(employee_match, employees["rows"]))

# Task 6
#---------------------------------------------------------------
def employee_find_2(employee_id):
    return list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))

# Task 7
#---------------------------------------------------------------
def sort_by_last_name():
    last_name_col = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_col])
    return employees["rows"]

# Task 8
#---------------------------------------------------------------
def employee_dict(row):
    skip_column = "employee_id"
    return {field: value for field, value in zip(employees["fields"], row)
            if field != skip_column}

# Task 9
#---------------------------------------------------------------
def all_employees_dict():
    emp_id_col = employee_id_column
    return {row[emp_id_col]: employee_dict(row) for row in employees["rows"]}

# Task 10
#---------------------------------------------------------------
def get_this_value():
    return os.getenv("THISVALUE")

# Task 11
#---------------------------------------------------------------
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

# Task 12
#---------------------------------------------------------------
def read_minutes():
    def read_minutes_file(filename):
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                fields = next(reader)
                rows = [tuple(row) for row in reader]
                return {'fields': fields, 'rows': rows}
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.", file=sys.stderr)
            sys.exit(1)
        except csv.Error as e:
            print(f"CSV parsing error in {filename}: {e}", file=sys.stderr)
            sys.exit(1)

    global minutes1, minutes2  
    
    minutes1 = read_minutes_file('../csv/minutes1.csv')
    minutes2 = read_minutes_file('../csv/minutes2.csv')

    return minutes1, minutes2

# Task 13
#---------------------------------------------------------------
def create_minutes_set():
    global minutes_set

    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])

    minutes_set = set1.union(set2)
    
    return minutes_set

# Task 14
#---------------------------------------------------------------
def create_minutes_list():
    global minutes_list  
    
    minutes_list = list(map(
        lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")),
        list(minutes_set))
    )
    
    return minutes_list

# Task 15
#---------------------------------------------------------------
def write_sorted_list():
    global minutes_list  
    
    minutes_list.sort(key=lambda x: x[1])
    
    sorted_list = [
        (name, date.strftime("%B %d, %Y")) 
        for name, date in minutes_list
    ]
    
    with open('../minutes.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header from minutes1
        writer.writerow(minutes1["fields"])
        # Write all rows
        writer.writerows(sorted_list)
    
    return sorted_list

def main():

    # Initialization of data
    global employees, minutes1, minutes2, minutes_set, minutes_list

    # Task 2
    employees = read_employees()

    # Task 3
    employee_id_column = column_index("employee_id")

    # Task 7
    sort_by_last_name()

    # Task 9
    employees_by_id = all_employees_dict()
    print("Employees dictionary:", employees_by_id)

    # Task 10-11
    print("THISVALUE:", get_this_value())
    set_that_secret("new_secret_value")
    print("Custom module secret:", custom_module.secret)

    # Task 12-15
    minutes1, minutes2 = read_minutes()
    minutes_set = create_minutes_set()
    minutes_list = create_minutes_list()
    sorted_minutes = write_sorted_list()
    print("Sorted minutes saved to minutes.csv")

if __name__ == "__main__":
    main()
