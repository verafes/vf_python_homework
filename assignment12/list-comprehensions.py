import pandas as pd

# Task 3.

df = pd.read_csv("../csv/employees.csv")

employee_names = [f"{row['first_name']} {row['last_name']}" for inx, row in df.iterrows()]
print(employee_names)

filtered_names = [name for name in employee_names if "e" in name.lower()]
print(filtered_names)
