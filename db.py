import sqlite3

connect = sqlite3.connect('grocery.sqlite3')
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

#Create user table
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            username TEXT NOT NULL UNIQUE,
            first_name TEXT,
            last_name TEXT,
            PRIMARY KEY (username)
        )""")

#Create registered registered user table
cursor.execute("""CREATE TABLE IF NOT EXISTS registeredusers(
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            address TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )""")

#Create admin user table
cursor.execute("""CREATE TABLE IF NOT EXISTS admin(
            admin_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            address TEXT NOT NULL,
            PRIMARY KEY (admin_id),
            FOREIGN KEY (username) REFERENCES users(username)
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
            PRIMARY KEY (order_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )""")

#Create cart table
cursor.execute("""CREATE TABLE IF NOT EXISTS cart(
            contents BLOB NOT NULL,
            user_id TEXT NOT NULL,
            cart_number INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(username)
            FOREIGN KEY (contents) REFERENCES groceries(item_id)
        )""")

#Create employee table
cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
            employee_id INTEGER NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            employer TEXT NOT NULL,
            PRIMARY KEY (employee_id)
            FOREIGN KEY (employer) REFERENCES supplier(name)
        )""")

#Create supplier table
cursor.execute("""CREATE TABLE IF NOT EXISTS suppliers(
            supplier_name TEXT NOT NULL,
            product TEXT NOT NULL,
            PRIMARY KEY (supplier_name)
            FOREIGN KEY (product) REFERENCES product(product_name)
        )""")

#Create product table
cursor.execute("""CREATE TABLE IF NOT EXISTS product(
            product_name TEXT NOT NULL,
            stock int NOT NULL,
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
    with open(fileName, 'rb') as file:
        img_data = file.read()
    return img_data

#Write image to file
def writeToFile(image, fileName):
    with open(fileName, 'wb') as file:
        file.write(image)

#Insert grocery item into groceries table
def add_item(item_id, item_name, item_img, category, stock, price):
    try:
        add_product(item_name, stock)
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        insert_query = """ INSERT INTO groceries
                        (item_id, item_name, item_img, category, stock, price) VALUES (?,?,?,?,?,?)"""
        image = cvt_image(item_img)
        data = (item_id, item_name, image, category, stock, price)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Item ID already exists")
    finally:
        if connection:
            connection.close()
          
#insert UNIQUE user into users table  

def add_user(username, first_name, last_name):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        insert_query = """INSERT INTO users VALUES (?, ?, ?)"""
        data = (username,first_name,last_name)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error) #prompt user to pick different username
    finally:
        if connection:
            connection.close()

def add_registereduser(username, password, first_name, last_name, address):
    try:
        add_user(username)
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()

        insert_query = """INSERT INTO registeredusers 
                        (username, password, name, address) VALUES (?, ?, ?, ?, ?)"""
        data = (username, password, first_name, last_name, address)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error)
    finally:
        if connection:
            connection.close()

def remove_user(username):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        delete_query = """DELETE FROM users WHERE username = ?"""
        data = (username,)
        cursor.execute(delete_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error) #prompt user to pick different username
    finally:
        if connection:
            connection.close()

def remove_registereduser(username):
    try:
        remove_user(username)
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        delete_query = """DELETE FROM registeredusers WHERE username = ?"""
        data = (username,)
        cursor.execute(delete_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error) #prompt user to pick different username
    finally:
        if connection:
            connection.close()

#fetch item from grocery table
def get_item(item_id):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
                
        fetch_query = """SELECT * from groceries where item_id = ?"""
        cursor.execute(fetch_query, (item_id,))
        record = cursor.fetchall()

        for row in record:
            name = row[1]
            image = row[2]
            imagePath = name + "1" + ".png"
            writeToFile(image, imagePath) #replace with store on website?
        cursor.close()
  
    except sqlite3.Error as error:
        print("whoopsies fetch")
    finally:
        if connection:
            connection.close()
            
#fetch user from users table
def get_user(username):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
                
        fetch_query = """SELECT * from registeredusers where username = ?"""
        cursor.execute(fetch_query, (username,))
        record = cursor.fetchall()

        for row in record:
            username = row[0]
            password = row[1]
            name = row[2]
            address = row[3]
        cursor.close()
  
    except sqlite3.Error as error:
        print("whoopsies fetch")
    finally:
        if connection:
            connection.close()

def login_user(username, password):
    db = connect()
    cursor = db.cursor()
    data = (username, password)
    cursor.execute((f"SELECT * FROM USER WHERE username=? AND password=?"), data)
    
    user = cursor.fetchall()
    if len(user) == 1:
        cursor.close()
        return True, user
    else:
        cursor.close()
        return False, None
    
def add_farm(farm_name, location):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        insert_query = """INSERT INTO farm 
                        (farm_name, location) VALUES (?, ?)"""
        data = (farm_name, location)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Farm already exists") #prompt user to pick different farm name
    finally:
        if connection:
            connection.close()

def add_product(product_name, stock):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        insert_query = """INSERT INTO product 
                        (product_name, stock) VALUES (?, ?)"""
        data = (product_name, stock)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Product already exists") #prompt user to pick different farm name
    finally:
        if connection:
            connection.close()

def remove_product(product_name):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        delete_query = """DELETE FROM product WHERE product_name = ?"""
        data = (product_name,)
        cursor.execute(delete_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error) #prompt user to pick different username
    finally:
        if connection:
            connection.close()

def add_sellsto(farm_name, supplier):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        insert_query = """INSERT INTO sellsto 
                        (farm_name, supplier) VALUES (?, ?)"""
        data = (farm_name, supplier)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Sells-to relationship already exists") #prompt user to pick different farm name
    finally:
        if connection:
            connection.close()

def add_employee(employee_id, first_name, last_name, employer):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        insert_query = """INSERT INTO employees 
                        (employee_id, first_name, last_name, employer) VALUES (?, ?, ?, ?)"""
        data = (employee_id, first_name, last_name, employer)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Sells-to relationship already exists") #prompt user to pick different farm name
    finally:
        if connection:
            connection.close()

def add_supplier(supplier_name, product):
    try:
        connection = sqlite3.connect('grocery.sqlite3')
        cursor = connection.cursor()
        insert_query = """INSERT INTO suppliers 
                        (supplier_name, product) VALUES (?, ?)"""
        data = (supplier_name, product)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error) #prompt user to pick different farm name
    finally:
        if connection:
            connection.close()
#test inserts/fetches
#add_item(1,"Bread", "images/bread.png", "Food", 12, 2.97)
#get_item(1)
#get_user("john")
#remove_registereduser("jon")
#add_product("banana", 15)
#remove_product("banana")
#add_registereduser("j", "pass1", "john", "123 john st")
#add_user("john", "pass2", "john", "123 john st")

#add_farm("Jimbob", "Calgary")
