import csv

with open('./csv/employees.csv', 'r') as file:
    reader = csv.reader(file)
    employees = list(reader)  

header = employees[0]
first_name_idx = header.index('first_name')
last_name_idx = header.index('last_name')

# Task 1: Create list of full names (first + space + last)
full_names = [
    f"{row[first_name_idx]} {row[last_name_idx]}"
    for row in employees[1:]  # Skip header row
]
print("All employee names:")
print(full_names)

# Task 2: Filter names containing 'e' 
names_with_e = [
    name
    for name in full_names
    if 'e' in name.lower()  
]
print("\nNames containing 'e':")
print(names_with_e)