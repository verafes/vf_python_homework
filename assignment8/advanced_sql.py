import sqlite3
import traceback
import os

db_dir = "../db"
print(os.path.dirname(os.path.realpath(__file__)))
os.makedirs(db_dir, exist_ok=True)

db_path = os.path.join(db_dir, "lesson.db")

try:
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        # Task 1
        statement1 = """
            SELECT orders.order_id, SUM(products.price * line_items.quantity) 
            FROM orders
            JOIN line_items ON orders.order_id = line_items.order_id
            JOIN products ON line_items.product_id = products.product_id
            GROUP BY orders.order_id
            ORDER BY orders.order_id
            LIMIT 5;
        """
        cursor.execute(statement1)
        results = cursor.fetchall()
        print("\n TASK 1:")
        for row in results:
            order_id, total = row
            print(f"Order ID: {order_id}, Total: ${total:.2f}")

        # Task 2
        statement2 = """
            SELECT orders.order_id, line_items.line_item_id, products.product_name 
            FROM orders 
            JOIN line_items ON orders.order_id = line_items.order_id 
            JOIN products ON products.product_id = line_items.product_id
            WHERE orders.order_id IN ( SELECT order_id FROM orders ORDER BY order_id LIMIT 5);
        """
        cursor.execute(statement2)
        results = cursor.fetchall()
        print("\n TASK 2:")
        for row in results:
            print(f"Customer: {row[0]}, Average Order Price: {row[1]:.2f}")

except sqlite3.Error as e:
    print("SQL error:", e)
