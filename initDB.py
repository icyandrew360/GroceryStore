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

print("completed db setup.")