# Task 6: Read Data into a DataFrame

import pandas as pd
import sqlite3

with sqlite3.connect("../db/lesson.db") as conn:

    statement = """
        SELECT l.line_item_id, l.quantity, l.product_id, p.product_name, p.price 
        FROM line_items l 
        JOIN products p ON l.product_id = p.product_id
    """
    df = pd.read_sql_query(statement, conn)

    # Task 6:3
    print("\n",df.head())

    # Task 6:4
    df['total'] = df['quantity'] * df['price']
    print("\n",df.head())

    # Task 6:5
    df = df.groupby('product_id').agg({'line_item_id': 'count', 'total': 'sum', 'product_name': 'first'})
    print("\n", df.head())

    # Task 6:6
    df = df.sort_values(by='product_name')
    print("\n", df.head())

    # Task 6:7
    df.to_csv("./order_summary.csv")