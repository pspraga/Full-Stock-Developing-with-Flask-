import sqlite3

conn=sqlite3.connect("Mydb.db")
cursor=conn.cursor()

def init_db():
    cursor.execute(
        """
create table if not exists Usermaster(id integer primary key,username TEXT NOT NULL,password TEXT NOT NULL)
"""
    )
    #cursor.execute("insert into usermaster(username,password) values(?,?)",("praga","1234"))
    #cursor.execute("delete from usermaster")
    conn.commit()
