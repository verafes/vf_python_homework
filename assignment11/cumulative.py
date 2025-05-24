import traceback
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

import plotly.express as px
import plotly.data as pldata


try:
    with sqlite3.connect("../db/lesson.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        # SQL query to get total price per order
        query = """
            SELECT o.order_id, SUM(p.price * l.quantity) AS total_price
            FROM orders o
            JOIN line_items l ON o.order_id = l.order_id
            JOIN products p ON l.product_id = p.product_id
            GROUP BY o.order_id
            ORDER BY o.order_id
        """

        # Read query result into DataFrame
        df_cumulative = pd.read_sql_query(query, conn)
        print(df_cumulative.head())

        # Task 2: A Line Plot with Pandas
        # Option 1
        # def cumulative(row):
        #     totals_above = df['total_price'][0:row.name+1]
        #     return totals_above.sum()
        # df['cumulative'] = df.apply(cumulative, axis=1)

        # Option 2: Using built-in cumsum
        df_cumulative['cumulative'] = df_cumulative['total_price'].cumsum()

        # Plotting
        df_cumulative.plot(
            kind='line',
            x='order_id',
            y='cumulative',
            title='Cumulative Revenue by Order',
            marker='o',
            color='green'
        )
        plt.xlabel('Order ID')
        plt.ylabel('Cumulative Revenue')
        plt.tight_layout(pad=2.0)
        plt.grid(True)
        plt.show()

        #Task 3
        df = pldata.wind(return_type='pandas')
        print(df.head(10))
        print(df.tail(10))

        df['strength'] = df['strength'].str.replace('[^0-9.]', '', regex=True).astype(float)
        fig = px.scatter(
            df, x='strength',
            y='frequency',
            color='direction',
            title='Wind Strength vs Frequency')
        fig.write_html("wind.html", auto_open=True)

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