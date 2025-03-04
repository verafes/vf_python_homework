import csv
import traceback
import os
from datetime import datetime

def read_employees():
    employees = {}
    rows = []
    try:
        with open("../csv/employees.csv", "r", newline="") as file:
            reader = csv.reader(file)
            first = True
            for row in reader:
                if first:
                    employees["fields"] = row
                    first=False
                else: 
                    rows.append(row)
            employees["rows"] = rows
        return employees
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")

employees = read_employees()
print("employees: ", employees)

def column_index(column_name):
    return employees["fields"].index(column_name)

employee_id_column=column_index("employee_id")

def first_name(row_number):
    first_name_index = column_index("first_name")
    return employees["rows"][row_number][first_name_index]

def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    return list(filter(employee_match, employees["rows"]))

def employee_find_2(employee_id):
    return list(filter(lambda row : int(row[employee_id_column]) == employee_id, employees["rows"]))

def sort_by_last_name():
    last_name_index = column_index("last_name")
    employees["rows"].sort(key = lambda row : row[last_name_index])
    return employees["rows"]

sort_by_last_name()
print("After sort: ", employees)

def employee_dict(row):
    return_dict = {}
    for i, field in enumerate(employees["fields"]):
        if field != "employee_id":
            return_dict[field] = row[i]
    return return_dict

print("employee_dict: ", employee_dict(employees["rows"][2]))

def all_employees_dict():
    return_dict = {}
    for row in employees["rows"]:
        return_dict[row[employee_id_column]]=employee_dict(row)
    return return_dict

print("all_employees_dict: ", all_employees_dict())

def get_this_value():
    return os.getenv("THISVALUE")

import custom_module
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret("open, sesame!")
print("module secret now: ", custom_module.secret)

def read_minutes():
    dict1 = {}
    dict2 = {}
    with open("../csv/minutes1.csv") as file:
        reader = csv.reader(file)
        list1 = []
        first = True
        for row in reader:
            if first:
                dict1["fields"] = row
                first = False
            else:
                list1.append(tuple(row))
        dict1["rows"] = list1
    with open("../csv/minutes2.csv") as file:
        reader = csv.reader(file)
        list1 = []
        first = True
        for row in reader:
            if first:
                dict2["fields"] = row
                first = False
            else:
                list1.append(tuple(row))
        dict2["rows"] = list1
    return dict1,dict2

minutes1, minutes2 = read_minutes()

print(minutes1, minutes2)

def create_minutes_set():
    return set(minutes1["rows"]).union(set(minutes2["rows"]))

minutes_set = create_minutes_set()
print(minutes_set)

def create_minutes_list():
    minutes_list1 = list(minutes_set)
    minutes_list1 = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list1))
    return minutes_list1

minutes_list = create_minutes_list()
print(minutes_list)

def write_sorted_list():
    minutes_list.sort(key= lambda x: x[1])
    minutes_list1 = list(map(lambda row: (row[0], datetime.strftime(row[1], "%B %-d, %Y")), minutes_list))
    with open("./minutes.csv","w") as file:
        writer = csv.writer(file)
        writer.writerow(minutes1["fields"])
        for row in minutes_list1:
            writer.writerow(row)
    return minutes_list1

write_sorted_list()