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
        print("TASK 1:")
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
        print("\nTASK 2:")
        for row in results:
            print(f"Customer: {row[0]}, Average Order Price: {row[1]:.2f}")

except sqlite3.Error as e:
    print("SQL error:", e)

# Task 3. Creating order for Perez and Sons
try:
    with sqlite3.connect(db_path) as conn:
        print("\nTASK 3:")
        print("\nCreating order for Perez and Sons")

        # retrieve the customer_id
        statement3 = """
            SELECT customer_id 
            FROM customers 
            WHERE customer_name = 'Perez and Sons'
        """
        cursor.execute(statement3)
        customer_id = cursor.fetchone()[0]
        print("3.1. Customer ID:", customer_id)

        # product_ids of the 5 least expensive products
        statement4 = """
            SELECT product_id 
            FROM products 
            ORDER BY price 
            DESC LIMIT 5
        """
        cursor.execute(statement4)
        products = cursor.fetchall()
        product_ids = [row[0] for row in products]
        print("\n3.2. Product_ids of the 5 least expensive product:")
        print(", ".join(map(str, product_ids)))

        # employee_id of Miranda Harris
        statement5 = """
            SELECT employee_id 
            FROM employees 
            WHERE first_name = 'Miranda' AND last_name = 'Harris'
        """
        cursor.execute(statement5)
        employee_id = cursor.fetchone()[0]
        print("\n3.3. Miranda Harris' Employee ID:", employee_id)

        # create the order record
        statement6 = """
            INSERT INTO orders (customer_id, employee_id)
            VALUES (?, ?)
            RETURNING order_id;
        """
        cursor.execute(statement6, (customer_id, employee_id))
        order_id = cursor.fetchone()[0]
        # print("\n3.4. Order:", order_id)

        # Insert line_items (10 units of each product)
        for product_id in product_ids:
            cursor.execute("""
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, ?);
            """, (order_id, product_id, 10))
        conn.commit()
        print(f"\n3.4. Order {order_id} created with 5 line items.")

        statement8 = """
            SELECT line_items.line_item_id, line_items.quantity, products.product_name 
            FROM line_items JOIN products
            ON line_items.product_id = products.product_id 
            WHERE line_items.order_id = ?;
        """
        cursor.execute(statement8, (order_id,))
        result = cursor.fetchall()
        print("\n3.5. List of line_item_id, quantity, product name")
        for row in result:
            print(f"{row[0]}, {row[1]}, {row[2]}")
except Exception as e:
    conn.rollback()
    print(f"Transaction failed: {e}")

# Task 4: Aggregation with HAVING
try:
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        statement = """
            SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
            FROM employees e 
            JOIN orders o ON e.employee_id = o.employee_id 
            GROUP BY e.employee_id 
            HAVING COUNT(order_id) > 5;
        """

        cursor.execute(statement)
        result = cursor.fetchall()

        print("\nTASK 4 : All employees associated with more than 5 orders. ")
        print(f"ID, Name, Orders count:")
        for row in result:
            employee_id, first_name, last_name, order_count = row
            print(f"{employee_id}, {first_name} {last_name}, {order_count} orders")


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