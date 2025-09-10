import sqlite3
import os

# Database path - assuming the database is in a 'db' folder one level up
DB_PATH = os.path.join('..', 'db', 'lesson.db')

# -------------------------------------------------------------------
# TASK 1: Complex JOINs with Aggregation
# -------------------------------------------------------------------
def task1_order_totals():

    print("\n====== TASK 1: ======")
    print("---------------------------------------")
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # SQL query to join 3 tables and calculate totals
        sql = """
        SELECT 
            orders.order_id,
            SUM(products.price * line_items.quantity) as total_price
        FROM orders
        JOIN line_items ON orders.order_id = line_items.order_id
        JOIN products ON line_items.product_id = products.product_id
        GROUP BY orders.order_id
        ORDER BY orders.order_id
        LIMIT 5
        """
        
        # Execute query
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # Display results
        if results:
            print("Order ID | Total Price")
            print("---------|------------")
            for order_id, total in results:
                print(f"{order_id:8} | ${total:.2f}")
        else:
            print("No orders found in database")
            
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# -------------------------------------------------------------------
# TASK 2: Subqueries
# -------------------------------------------------------------------
def task2_customer_averages():

    print("\n====== TASK 2: ======")
    print("----------------------------------------------------------")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # SQL with subquery - calculates order totals first, then averages
        sql = """
        SELECT 
            customers.customer_name,
            AVG(order_totals.total_price) as avg_value
        FROM customers
        LEFT JOIN (
            SELECT 
                orders.customer_id,
                SUM(products.price * line_items.quantity) as total_price
            FROM orders
            JOIN line_items ON orders.order_id = line_items.order_id
            JOIN products ON line_items.product_id = products.product_id
            GROUP BY orders.order_id
        ) AS order_totals ON customers.customer_id = order_totals.customer_id
        GROUP BY customers.customer_id
        ORDER BY avg_value DESC
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if results:
            print("Customer Name      | Average Value")
            print("-------------------|--------------")
            for name, avg_value in results:
                if avg_value:
                    print(f"{name:<18} | ${avg_value:.2f}")
                else:
                    print(f"{name:<18} | No orders")
        else:
            print("No customers found")
            
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# -------------------------------------------------------------------
# TASK 3: Transaction Example
# -------------------------------------------------------------------
def task3_create_order():

    print("\n====== TASK 3: ======")
    print("--------------------------------------------------")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Start transaction
        conn.execute("BEGIN TRANSACTION")
        
        # Get customer ID
        cursor.execute("SELECT customer_id FROM customers WHERE customer_name LIKE '%Perez%' LIMIT 1")
        customer = cursor.fetchone()
        if not customer:
            print("Perez customer not found")
            conn.rollback()
            return
        customer_id = customer[0]
        
        # Get employee ID
        cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' LIMIT 1")
        employee = cursor.fetchone()
        if not employee:
            print("Miranda employee not found")
            conn.rollback()
            return
        employee_id = employee[0]
        
        # Get cheapest products
        cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
        products = [row[0] for row in cursor.fetchall()]
        
        # Create order
        cursor.execute("INSERT INTO orders (customer_id, employee_id, order_date) VALUES (?, ?, date('now'))", 
                      (customer_id, employee_id))
        order_id = cursor.lastrowid
        
        # Add line items
        for product_id in products:
            cursor.execute("INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, 10)", 
                          (order_id, product_id))
        
        # Commit transaction
        conn.commit()
        print(f"Success! Created order #{order_id} with {len(products)} items")
        
    except sqlite3.Error as e:
        print(f"Transaction failed: {e}")
        conn.rollback()
    finally:
        conn.close()

# -------------------------------------------------------------------
# TASK 4: HAVING Clause
# -------------------------------------------------------------------
def task4_busy_employees():

    print("\n====== TASK 4: ======")
    print("-------------------------------------")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # SQL with HAVING clause
        sql = """
        SELECT 
            employees.first_name,
            employees.last_name,
            COUNT(orders.order_id) as order_count
        FROM employees
        JOIN orders ON employees.employee_id = orders.employee_id
        GROUP BY employees.employee_id
        HAVING COUNT(orders.order_id) > 5
        ORDER BY order_count DESC
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if results:
            print("First Name | Last Name  | Orders")
            print("-----------|------------|--------")
            for first, last, count in results:
                print(f"{first:10} | {last:10} | {count:6}")
        else:
            print("No employees with more than 5 orders")
            
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# -------------------------------------------------------------------
# Run the tasks one by one
# -------------------------------------------------------------------

task1_order_totals()
task2_customer_averages() 
task3_create_order()
task4_busy_employees()

print("\nAll tasks completed!")