import mysql.connector
from mysql.connector import Error
import hashlib
from dotenv import load_dotenv
import os

load_dotenv()
database_pwd = os.getenv('DATABASE_PWD')
database_user=os.getenv('DATABASE_USER')
admin_username=os.getenv('ADMIN_USERNAME')
admin_password=os.getenv('ADMIN_PASSWORD')

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=database_user,
            password=database_pwd,
            database='employee_management'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_employee_login(cursor, email, password):
    hashed_password = hash_password(password)
    query = "SELECT * FROM employees WHERE email = %s AND password = %s"
    cursor.execute(query, (email, hashed_password))
    return cursor.fetchone()

def get_employee_by_id(cursor, emp_id):
    query = "SELECT * FROM employees WHERE id = %s"
    cursor.execute(query, (emp_id,))
    return cursor.fetchone()

def get_all_employees(cursor):
    query = "SELECT * FROM employees"
    cursor.execute(query)
    return cursor.fetchall()

def modify_employee(cursor, emp_id, name=None, salary=None, dept=None, password=None):
    update_fields = []
    params = []
    
    if name:
        update_fields.append("name = %s")
        params.append(name)
    if salary:
        update_fields.append("salary = %s")
        params.append(salary)
    if dept:
        update_fields.append("dept = %s")
        params.append(dept)
    if password:
        update_fields.append("password = %s")
        params.append(hash_password(password))
    
    params.append(emp_id)
    
    if update_fields:
        query = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, tuple(params))
        connection.commit()  # Commit the changes

def add_employee(cursor, email, name, password, salary, dept):
    hashed_password = hash_password(password)
    query = "INSERT INTO employees (email, name, password, salary, dept) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (email, name, hashed_password, salary, dept))
    connection.commit()  # Commit the changes

def delete_employee(cursor, emp_id):
    query = "DELETE FROM employees WHERE id = %s"
    cursor.execute(query, (emp_id,))
    connection.commit()  # Commit the changes

def admin_operations(cursor):
    while True:
        print("\nAdmin Menu:")
        print("1. Add Employee")
        print("2. View Employee Details")
        print("3. View All Employees")
        print("4. Delete Employee")
        print("5. Modify Employee")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            email = input("Enter email: ")
            name = input("Enter name: ")
            password = input("Enter password: ")
            salary = float(input("Enter salary: "))
            dept = input("Enter department: ")
            add_employee(cursor, email, name, password, salary, dept)
            print("Employee added successfully!")
        
        elif choice == '2':
            emp_id = int(input("Enter employee id: "))
            employee = get_employee_by_id(cursor, emp_id)
            if employee:
                print(f"Employee Details: {employee}")
            else:
                print("Employee not found.")
        
        elif choice == '3':
            employees = get_all_employees(cursor)
            if employees:
                print("All Employees:")
                for emp in employees:
                    print(emp)
            else:
                print("No employees found.")
        
        elif choice == '4':
            emp_id = int(input("Enter employee id to delete: "))
            employee = get_employee_by_id(cursor, emp_id)
            if employee:
                delete_employee(cursor, emp_id)
                print("Employee deleted successfully!")
            else:
                print("Employee not found. Cannot delete.")
        
        elif choice == '5':
            emp_id = int(input("Enter employee id to modify: "))
            employee = get_employee_by_id(cursor, emp_id)
            if employee:
                name = input("Enter new name (press Enter to skip): ")
                salary = input("Enter new salary (press Enter to skip): ")
                dept = input("Enter new department (press Enter to skip): ")
                password = input("Enter new password (press Enter to skip): ")
                modify_employee(cursor, emp_id, name, salary, dept, password)
                print("Employee details updated successfully!")
            else:
                print("Employee not found. Cannot modify.")
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice. Please try again.")

def employee_operations(cursor, emp_id):
    while True:
        print("\nEmployee Menu:")
        print("1. View Details")
        print("2. Modify Details")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            employee = get_employee_by_id(cursor, emp_id)
            if employee:
                print(f"Employee Details: {employee}")
            else:
                print("Employee not found.")
        
        elif choice == '2':
            name = input("Enter new name (press Enter to skip): ")
            salary = input("Enter new salary (press Enter to skip): ")
            dept = input("Enter new department (press Enter to skip): ")
            password = input("Enter new password (press Enter to skip): ")
            modify_employee(cursor, emp_id, name, salary, dept, password)
            print("Employee details updated successfully!")
        
        elif choice == '3':
            break
        
        else:
            print("Invalid choice. Please try again.")

def main():
    global connection  
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        print()
        print("                                                  Employee Management System")
        print()
        input("Press Enter to Continue")
        print()
        user_type = input("Are you an 'admin' or 'employee'? ").strip().lower()
        
        if user_type == 'admin':
            admin_username = input("Enter admin username: ")
            admin_password = input("Enter admin password: ")
            # Assuming admin credentials validation
            if admin_username ==admin_username  and admin_password ==admin_password :
                admin_operations(cursor)
            else:
                print("Invalid admin credentials.")
        
        elif user_type == 'employee':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            employee = check_employee_login(cursor, email, password)
            if employee:
                emp_id = employee[0]
                print("Employee login successful!")
                employee_operations(cursor, emp_id)
            else:
                print("Invalid employee credentials.")
        
        else:
            print("Invalid user type.")
        
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()




