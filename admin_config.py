import sqlite3

def add_admin(username):
    connection = sqlite3.connect('lib/grocery.sqlite3')
    cursor = connection.cursor()

    insert_query = """INSERT INTO admin 
                    (admin_user) VALUES (?)"""
    data = (username,)
    cursor.execute(insert_query, data)
    print('Executed query.')
    connection.commit()
    cursor.close()

def isUserAdmin(username):
    connection = sqlite3.connect('lib/grocery.sqlite3')
    cursor = connection.cursor()
    data = (username,)
    cursor.execute((f"SELECT * FROM admin WHERE admin_user=?"), data)
    
    user = cursor.fetchall()
    if len(user) == 1:
        cursor.close()
        return True
    else:
        cursor.close()
        return False

#add_admin('icyandrew')