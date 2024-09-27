import sqlite3

conn=sqlite3.connect("Mydb.db")
cursor=conn.cursor()
#cursor.execute("drop table Usermaster")
conn.commit()
def init_db():
    
    cursor.execute(
        """
create table if not exists Usermaster(id integer primary key,username TEXT NOT NULL,password TEXT NOT NULL,email TEXT NULL,Role TEXT NOT NULL)
"""
    )
    cursor.execute(
        """
create table if not exists shipping(tracking_no TEXT NOT NULL,shipping TEXT NOT NULL,destination TEXT NULL)
"""
    )
    #cursor.execute("insert into usermaster(username,password,Role) values(?,?,?)",("praga","1234","admin"))
    #cursor.execute("delete from usermaster")
    #cursor.execute("drop table Usermaster")
    conn.commit()