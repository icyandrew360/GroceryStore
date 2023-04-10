import sqlite3
import random
import datetime

connect = sqlite3.connect('lib/grocery.sqlite3')
cursor = connect.cursor()

#Create groceries table
cursor.execute("""CREATE TABLE IF NOT EXISTS groceries (
            item_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            item_img BLOB NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER NOT NULL,
            price REAL NOT NULL,
            PRIMARY KEY (item_id),
            FOREIGN KEY(item_name) REFERENCES product(product_name)
        )""")

#Create registered registered user table
cursor.execute("""CREATE TABLE IF NOT EXISTS registeredusers(
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            address TEXT NOT NULL,
            PRIMARY KEY (username)
        )""")

#Create admin user table
cursor.execute("""CREATE TABLE IF NOT EXISTS admin(
            admin_user TEXT NOT NULL,
            FOREIGN KEY (admin_user) REFERENCES users(username)
            PRIMARY KEY (admin_user)
        )""")

#Create order table
cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            shipping_address TEXT NOT NULL,
            PRIMARY KEY (order_id),
            FOREIGN KEY (username) REFERENCES users(username)
        )""")

#Create receipt table
cursor.execute("""CREATE TABLE IF NOT EXISTS receipt(
            order_id INTEGER NOT NULL,
            total REAL NOT NULL,
            date DATE NOT NULL,
            shipping_address TEXT NOT NULL,
            PRIMARY KEY (order_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )""")

#Create cart table
cursor.execute("""CREATE TABLE IF NOT EXISTS cart(
            username TEXT NOT NULL,
            cart_number INTEGER NOT NULL,
            item INTEGER NOT NULL, 
            FOREIGN KEY (username) REFERENCES users(username)
            FOREIGN KEY (item) REFERENCES groceries(item_id)
        )""")

#Create employee table
cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
            employee_id INTEGER NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            employer TEXT NOT NULL,
            PRIMARY KEY (employee_id)
            FOREIGN KEY (employer) REFERENCES supplier(supplier_name)
        )""")

#Create supplier table
cursor.execute("""CREATE TABLE IF NOT EXISTS suppliers(
            supplier_name TEXT NOT NULL,
            product TEXT NOT NULL,
            PRIMARY KEY (supplier_name)
            FOREIGN KEY (product) REFERENCES product(product_name)
        )""")

#Create product table
cursor.execute("""
            CREATE TABLE IF NOT EXISTS product(
            product_name TEXT NOT NULL,
            stock int NOT NULL,
            price FLOAT NOT NULL,
            PRIMARY KEY (product_name)
        )""")

#Create product table
cursor.execute("""CREATE TABLE IF NOT EXISTS supplies(
            supplier TEXT NOT NULL,
            grocery_item TEXT NOT NULL,
            FOREIGN KEY (supplier) REFERENCES suppliers(supplier_name)
            FOREIGN KEY (grocery_item) REFERENCES groceries(item_id)
        )""")

#Create farm table
cursor.execute("""CREATE TABLE IF NOT EXISTS farm(
            farm_name TEXT NOT NULL,
            location TEXT NOT NULL,
            PRIMARY KEY (farm_name)
        )""")

#Create sells to table
cursor.execute("""CREATE TABLE IF NOT EXISTS sellsto(
            farm_name TEXT NOT NULL,
            supplier TEXT NOT NULL,
            FOREIGN KEY (supplier) REFERENCES suppliers(supplier_name)
            FOREIGN KEY (farm_name) REFERENCES farm(farm_name)
        )""")

connect.close()

#Convert image into bits to be stored
def cvt_image(fileName):
    with open(fileName, 'rb') as file: #open filepath
        img_data = file.read() #read data
    return img_data

#Write image to file
def writeToFile(image, fileName):
    with open(fileName, 'wb') as file: #create new file
        file.write(image) #write image to file

#Insert grocery item into groceries table
def add_item(item_id, item_name, item_img, category, stock, price):
    connection = None #initialize connection
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """ INSERT INTO groceries
                        (item_id, item_name, item_img, category, stock, price) VALUES (?,?,?,?,?,?)""" #insert query
        #image = cvt_image(item_img) #get image bytes from filepath
        data = (item_id, item_name, item_img, category, stock, price) #insert data into query
        cursor.execute(insert_query, data) #execute query
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting towhen attempting to add item
    finally:
        if connection:
            connection.close() #close connection to sql database 
    return

#get item from grocery table
def get_item(item_id):
    connection = None
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        fetch_query = """SELECT * from groceries where item_id = ?""" #query to get item from database
        cursor.execute(fetch_query, (item_id,))
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
  
    except sqlite3.Error as error:
        print(error) #error occurred
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def remove_item(item_id):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM groceries WHERE item_id = ?""" #query to remove item from database
        data = (item_id,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to remove grocery item
    finally:
        if connection:
            connection.close() #close connection to sql database
    return

def getItemPrice(item_name):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT price FROM product where product_name = ?""" #query to get item price from database
        cursor.execute(fetch_query, (item_name,))
        record = cursor.fetchall() #get results from query

        if len(record) == 0:
            print("ERROR: ITEM NOT FOUND IN DB")
            return ()
        price = record[0][0]
        cursor.close() #close cursor
        return (float(price))
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get item price
    finally:
        if connection:
            connection.close() #close connection to sql database

def create_order_id(): #helper function for creating new order
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor  
        while(1):
            random_number = random.randint(0, 2147483647)
            fetch_query = """SELECT * from orders where order_id = ?""" #query to get order ID from database
            cursor.execute(fetch_query, (random_number,))
            record = cursor.fetchall() #get results from query
            if(record == [] or record is None):
                return random_number
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to create order ID
    finally:
        if connection:
            connection.close() #close connection to sql database
    
def checkout(username, address, total): #create order and receipt
    try:
        order_id = create_order_id()
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """INSERT INTO orders 
                        (order_id, username, shipping_address) VALUES (?, ?, ?)""" #query to get insert order into database
        data = (order_id, username, address)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        date = datetime.datetime.now()
        insert_query = """INSERT INTO receipt 
                        (order_id, total, date, shipping_address) VALUES (?, ?, ?, ?)""" #query to insert receipt into database
        data = (order_id, total, date, address)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to checkout user
    finally:
        if connection:
            connection.close() #close connection to sql database
    
def remove_order(order_id): #delete order and receipt
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM orders WHERE order_id = ?""" #query to remove order from database
        data = (order_id,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        delete_query = """DELETE FROM receipt WHERE order_id = ?""" #query to remove order from database
        data = (order_id,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to remove order from database
    finally:
        if connection:
            connection.close() #close connection to sql database
    
def get_orders(username):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT * from orders where username = ?""" #query to get order from database
        cursor.execute(fetch_query, (username,))
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
  
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get orders
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def add_employee(employee_id, first_name, last_name, employer): #add to employee table
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """INSERT INTO employees 
                        (employee_id, first_name, last_name, employer) VALUES (?, ?, ?, ?)""" #query to insert employee into database
        data = (employee_id, first_name, last_name, employer)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to add employees
    finally:
        if connection:
            connection.close() #close connection to sql database
            
def remove_employee(employee_id):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM employees WHERE employee_id = ?""" #query to remove employee from database
        data = (employee_id,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to remove employee
    finally:
        if connection:
            connection.close() #close connection to sql database
    return

def get_employee(employee_id):
    connection = None
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT * from employees where employee_id = ?""" #query to get employee from database
        cursor.execute(fetch_query, (employee_id,))
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
  
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get employee
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def get_all_employees():
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT * from employees""" #query to get order from database
        cursor.execute(fetch_query)
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
  
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get orders
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def add_supplier(supplier_name, product): #add to suppliers table
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """INSERT INTO suppliers 
                        (supplier_name, product) VALUES (?, ?)""" #query to get supplier from database
        data = (supplier_name, product)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to add supplier
    finally:
        if connection:
            connection.close() #close connection to sql database
        
def remove_supplier(supplier_name):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM suppliers WHERE supplier_name = ?""" #query to remove supplier from database
        data = (supplier_name,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to remove supplier
    finally:
        if connection:
            connection.close() #close connection to sql database
    return

def get_supplier(supplier_name):
    connection = None
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        fetch_query = """SELECT * from suppliers where supplier_name = ?""" #query to get supplier from database
        cursor.execute(fetch_query, (supplier_name,))
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get supplier
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record


def get_all_suppliers():
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT * from suppliers""" #query to get order from database
        cursor.execute(fetch_query)
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
  
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get orders
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record


def add_supplies(supplier, grocery_item):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """INSERT INTO supplies 
                        (supplier, grocery_item) VALUES (?, ?)""" #query to insert supplies into database
        data = (supplier, grocery_item)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to add supplies
    finally:
        if connection:
            connection.close() #close connection to sql database

def remove_supplies(supplier, grocery_item):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM supplies WHERE supplier = ? AND grocery_item = ?""" #query to delete supplies from database
        data = (supplier, grocery_item)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to remove supplies
    finally:
        if connection:
            connection.close() #close connection to sql database
    return


def add_farm(farm_name, location): #add to farm table
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """INSERT INTO farm 
                        (farm_name, location) VALUES (?, ?)""" #query to add farm to database
        data = (farm_name, location)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to add farm
        if connection:
            connection.close() #close connection to sql database
            
def remove_farm(farm_name):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM farm WHERE farm_name = ?""" #query to remove farm from database
        data = (farm_name,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to remove farm
    finally:
        if connection:
            connection.close() #close connection to sql database
    return

def get_farm(farm_name):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT * from farm where farm_name = ?""" #query to get farm from database
        cursor.execute(fetch_query, (farm_name,))
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get farm
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def get_all_farms():
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT * from farm""" #query to get order from database
        cursor.execute(fetch_query)
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
  
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get orders
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def add_sellsto(farm_name, supplier): #add to sellsto table
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """INSERT INTO sellsto 
                        (farm_name, supplier) VALUES (?, ?)""" #query to add sellsto to database
        data = (farm_name, supplier)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to add sellsto
        if connection:
            connection.close() #close connection to sql database
            
def remove_sellsto(farm_name, supplier):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM sellsto WHERE farm_name = ? AND supplier = ?""" #query to remove sellsto from database
        data = (farm_name, supplier)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when remove sellsto
    finally:
        if connection:
            connection.close() #close connection to sql database
    return

def add_product(product_name, stock, price): #add to product table
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """INSERT INTO product 
                        (product_name, stock, price) VALUES (?, ?, ?)""" #query to insert product into database
        data = (product_name, stock, price)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
        print(f"added product {product_name}, amount: {stock}, price: {price}")
    except sqlite3.Error as error:
        print(error) #error occurred when attempting add product
    finally:
        if connection:
            connection.close() #close connection to sql database

def remove_product(product_name): #remove from product table
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM product WHERE product_name = ?""" #query to remove product from database
        data = (product_name,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when remove product
    finally:
        if connection:
            connection.close() #close connection to sql database

def get_product(product_name):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT * from product where product_name = ?""" #query to get product from database
        cursor.execute(fetch_query, (product_name,))
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get product
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def add_admin(admin_user):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """INSERT INTO admin 
                        (admin_user) VALUES (?)""" #query to add admin into database
        data = (admin_user,)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to add admin
    finally:
        if connection:
            connection.close() #close connection to sql database
    return

def remove_admin(admin_user):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM admin WHERE admin_user = ?""" #query to remove admin from database
        data = (admin_user,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to remove admin
    finally:
        if connection:
            connection.close() #close connection to sql database
    return

def get_all_admins():
    try:
        connection =  sqlite3.connect('lib/grocery.sqlite3')
        cursor = connection.cursor()

        query = 'SELECT * FROM admin'
        cursor.execute(query)

        record = cursor.fetchall() 
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to add admin
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def get_all_registered_users():
    try:
        connection =  sqlite3.connect('lib/grocery.sqlite3')
        cursor = connection.cursor()

        query = 'SELECT username FROM registeredusers'
        cursor.execute(query)

        record = cursor.fetchall() 
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to add admin
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def add_registereduser(username, password, first_name, last_name, address): #add registered user
    connection = None
    try:    
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor

        insert_query = """INSERT INTO registeredusers 
                        (username, password, first_name, last_name, address) VALUES (?, ?, ?, ?, ?)""" #query to add registereduser to database
        data = (username, password, first_name, last_name, address)
        cursor.execute(insert_query, data)
        print('Executed query.')
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        return False #registered user already exists!
    finally:
        if connection:
            connection.close() #close connection to sql database
            return True #successfully created user

def remove_user(username): #remove registered user
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM registeredusers WHERE username = ?""" #query to remove user from database
        data = (username,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to remove user
    finally:
        if connection:
            connection.close() #close connection to sql database

def get_user(username): #get registereduser
    connection = None
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT * from registeredusers where username = ?""" #query to get registered user from database
        cursor.execute(fetch_query, (username,))
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
  
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get user
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record

def add_to_cart(username, cart_number, item):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        insert_query = """INSERT INTO cart
                        (username, cart_number, item) VALUES (?,?,?)""" #query to add cart to database
        data = (username, cart_number, item)
        cursor.execute(insert_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to add to cart
    finally:
        if connection:
            connection.close() #close connection to sql database
    return

def remove_from_cart(username):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        delete_query = """DELETE FROM cart WHERE username = ?"""  #query to remove cart from database
        data = (username,)
        cursor.execute(delete_query, data)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to remove item from cart
    finally:
        if connection:
            connection.close() #close connection to sql database
    return

def get_cart(username):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT * from cart where username = ?"""  #query to get cart user from database
        cursor.execute(fetch_query, (username,))
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
  
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get cart contents
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record


def get_contents_of_cart(cart_number):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
                
        fetch_query = """SELECT item from cart where cart_number = ?"""  #query to items from a cart from the database
        cursor.execute(fetch_query, (cart_number,))
        record = cursor.fetchall() #get results from query
        cursor.close() #close cursor
  
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to get cart items
    finally:
        if connection:
            connection.close() #close connection to sql database
    return record


def login_user(username, password): #verify login information
    connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
    cursor = connection.cursor() #create new cursor
    data = (username, password)
    cursor.execute((f"SELECT * FROM registeredusers WHERE username=? AND password=?"), data)  #query to check if user exists in database
    
    user = cursor.fetchall()
    if len(user) == 1:
        cursor.close() #close cursor
        return True, user #user exists in the database. return user object
    else:
        cursor.close() #close cursor
        return False, None #user does not exist in database, return null

def increase_stock(product_name, amount):
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3') #connect to sql database
        cursor = connection.cursor() #create new cursor
        query = "SELECT stock FROM product WHERE product_name = ?"  #query to get stock from database
        cursor.execute(query, (product_name,))
        data = cursor.fetchall()
        currStock = data[0][0]
        currStock = currStock + amount
        if currStock < 0:
            return 'error occured: cant reduce stock to negative D:'
        query = """UPDATE product
                    SET stock = ? 
                    WHERE product_name = ?"""
        values = (currStock, product_name)
        cursor.execute(query, values)
        connection.commit() #commit changes to database
        cursor.close() #close cursor
        print(f"updated {product_name} stock to {currStock}")
    except sqlite3.Error as error:
        print(error) #error occurred when attempting to increase stock

def get_inventory_stock():
    try:
        connection = sqlite3.connect('lib/grocery.sqlite3')
        cursor = connection.cursor()
        query = " SELECT product_name, stock FROM product"
        cursor.execute(query)
        data = cursor.fetchall()
        return (data)
    except sqlite3.Error as error:
        print(error)