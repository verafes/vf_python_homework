import sqlite3
import traceback
import pandas as pd
import matplotlib.pyplot as plt

# Task 1 Plotting with Pandas
try:
    with sqlite3.connect("../db/lesson.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        query = """
            SELECT last_name, 
            SUM (price * quantity) AS revenue 
            FROM employees e 
            JOIN orders o ON e.employee_id = o.employee_id 
            JOIN line_items l ON o.order_id = l.order_id 
            JOIN products p ON l.product_id = p.product_id 
            GROUP BY e.employee_id;
        """

        df_employee = pd.read_sql_query(query, conn)
        # print(df_employee)

        # Display the DataFrame
        df_employee.plot(
            kind='bar',
            x='last_name',
            y='revenue',
            color='lightgreen',
            title='Employee Revenue')
        plt.xlabel('Employee')
        plt.ylabel('Revenue')

        plt.tight_layout(pad=2.0)
        # plt.xticks(rotation=45)
        plt.show()

except Exception as e:
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(
            f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")
else:
    print("All SQL operations completed.")
