import sqlite3

dbConn = sqlite3.connect("lib/store.db")
print("successful opening")

cursor = dbConn.cursor()

cursor.execute("DROP TABLE IF EXISTS Users")
cursor.execute("""
CREATE TABLE Users (
    email TEXT PRIMARY KEY,
    fname TEXT,
    lname TEXT,
    password TEXT,
    address TEXT
)
""")

cursor.execute("DROP TABLE IF EXISTS Items")
cursor.execute("""
CREATE TABLE Items(
    name TEXT PRIMARY KEY,
    stock INT
) 
""")

cursor.execute("DROP TABLE IF EXISTS Admins")
cursor.execute("""
CREATE TABLE Admins (
    peemail TEXT,
    email TEXT PRIMARY KEY,
    FOREIGN KEY (email) REFERENCES Users(email) ON DELETE CASCADE
)
""")
print("completed db setup.")