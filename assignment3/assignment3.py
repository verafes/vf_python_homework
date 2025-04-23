# %%
import pandas as pd

#Task 1. Create a DataFrame from a dictionary:
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)
print(f"task 1.1. data frame:\n {task1_data_frame}")

task1_with_salary = task1_data_frame.copy()

task1_with_salary["Salary"] = [70000, 80000, 90000]
print(f"task 1.2. df with salary\n {task1_with_salary}")

task1_older = task1_with_salary.copy()
task1_older["Age"] = task1_older["Age"]+1
print(f"task 1.3. older:\n {task1_older}")

task1_older.to_csv("employees.csv", index=False)

#Task 2.  Loading Data
task2_employees = pd.read_csv("employees.csv")
print(f"Task 2.1. Read from csv:\n {task2_employees}")

json_employees = pd.read_json("additional_employees.json")
print(f"Task 2.2. Read from json:\n {json_employees}")

more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print(f"Task 2.2. more_employees:\n {more_employees}")

#Task 3. Data Inspection
first_three = more_employees.head(3)
print(f"Task 3.1. first_three:\n {first_three}")

last_two = more_employees.tail(2)
print(f"Task 3.2. last_two:\n {last_two}")

employee_shape = more_employees.shape
print(f"Task 3.3. employee_shape:\n {employee_shape}")

print(f"Task 3.4. more_employees.info:")
more_employees.info()

#Task 4. Data Cleaning
dirty_data = pd.read_csv("dirty_data.csv")
print(f"Task 4.1. dirty_data:\n {dirty_data}")

clean_data = dirty_data.copy()
print(f"Task 4.2. clean_data:\n {clean_data}")

clean_data = clean_data.drop_duplicates()
print(f"Task 4.3. Remove duplicates:\n {clean_data}")

clean_data["Age"] = pd.to_numeric(clean_data["Age"], errors="coerce")
print(f"Task 4.3. Convert Age to numeric:\n {clean_data}")

clean_data["Salary"] = clean_data["Salary"].replace(["unknown", "n/a"], pd.NA)
print(f"Task 4.4. Replace unknown, n/a with NaN:\n {clean_data}")
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"], errors="coerce")
print(f"Task 4.4. Salary to numeric:\n {clean_data}\n")

mean_age = clean_data["Age"].mean()
clean_data["Age"] = clean_data["Age"].fillna(mean_age)
median_salary = clean_data["Salary"].median()
clean_data["Salary"] = clean_data["Salary"].fillna(median_salary)
print(f"Task 4.5. Fill missing numeric values:\n {clean_data}")

clean_data["Hire Date"] = pd.to_datetime(clean_data["Hire Date"], errors="coerce")
print(f"Task 4.6. Convert Hire Date to datetime:\n {clean_data}")

clean_data["Department"] = clean_data["Department"].str.strip().str.upper()
clean_data["Name"] = clean_data["Name"].str.strip()
clean_data["Name"] = clean_data["Name"].str.upper()
print(f"Task 4.7. Strip extra whitespace and uppercase:\n {clean_data}")