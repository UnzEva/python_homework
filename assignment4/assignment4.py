import pandas as pd
import json
import numpy as np

# Task 1: Introduction to Pandas - Creating and Manipulating DataFrames
#-----------------------------------------------------------------------
# Create DataFrame from dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
task1_data_frame = pd.DataFrame(data)
print("Original DataFrame:")
print(task1_data_frame)
print()

# Add new column (Salary)
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print("DataFrame with Salary column:")
print(task1_with_salary)
print()

# Modify existing column (Age)
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1
print("DataFrame with incremented Age:")
print(task1_older)
print()

# Save to CSV
task1_older.to_csv('employees.csv', index=False)
print("DataFrame saved to employees.csv")

# Task 2: Loading Data from CSV and JSON
#---------------------------------------------------------
# Read data from CSV file (created in Task 1)
task2_employees = pd.read_csv('employees.csv')
print("Employees loaded from CSV:")
print(task2_employees)
print()

# Create and read from JSON file
additional_data = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]

with open('additional_employees.json', 'w') as f:
    json.dump(additional_data, f)

json_employees = pd.read_json('additional_employees.json')
print("Employees loaded from JSON:")
print(json_employees)
print()

# Combine DataFrames
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print("Combined Employees DataFrame:")
print(more_employees)

# Task 3: Data Inspection - Using Head, Tail, and Info Methods
#-------------------------------------------------------------------------------
# Use the head() method
first_three = more_employees.head(3)
print("First three employees:")
print(first_three)
print()

# Use the tail() method
last_two = more_employees.tail(2)
print("Last two employees:")
print(last_two)
print()

# Get the shape of the DataFrame
employee_shape = more_employees.shape
print("Shape of the DataFrame (rows, columns):")
print(employee_shape)
print()

# Use the info() method
print("DataFrame information:")
more_employees.info()

# Task 4: Data Cleaning
#-------------------------------------------------------------------------
# Load the dirty data
dirty_data = pd.read_csv('dirty_data.csv')
print("Original Dirty Data:")
print(dirty_data)
print("\n")

# Create a clean copy
clean_data = dirty_data.copy()

# Remove duplicates
clean_data = clean_data.drop_duplicates()
print("After removing duplicates:")
print(clean_data)
print("\n")

# Convert Age to numeric and handle missing values
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print("After converting Age to numeric:")
print(clean_data)
print("\n")

# Convert Salary to numeric and handle placeholders
salary_replacements = {'unknown': np.nan, 'n/a': np.nan}
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'].replace(salary_replacements), errors='coerce')
print("After cleaning Salary:")
print(clean_data)
print("\n")

# Fill missing numeric values
age_mean = clean_data['Age'].mean()
salary_median = clean_data['Salary'].median()
clean_data['Age'] = clean_data['Age'].fillna(age_mean)
clean_data['Salary'] = clean_data['Salary'].fillna(salary_median)
print("After filling missing values:")
print(clean_data)
print("\n")

# Convert Hire Date to datetime
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], format='mixed', errors='coerce')
print("After converting Hire Date:")
print(clean_data)
print("\n")

# Clean text columns
clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print("Final Cleaned Data:")
print(clean_data)
