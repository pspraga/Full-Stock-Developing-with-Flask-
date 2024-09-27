from flask import Flask,render_template,request,session,redirect,url_for,g,flash,jsonify
#from database import init_db
import sqlite3
#init_db()
conn=sqlite3.connect("Mydb.db",check_same_thread=False)
cur=conn.cursor()
cur.execute(
        """
create table if not exists Usermaster(id integer primary key,username TEXT NOT NULL,password TEXT NOT NULL,email TEXT NULL,Role TEXT NOT NULL)
"""
    )
cur.execute(
        """
create table if not exists shipping(tracking_no TEXT NOT NULL,shipping TEXT NOT NULL,destination TEXT NULL)
"""
    )
    #cursor.execute("insert into usermaster(username,password,Role) values(?,?,?)",("praga","1234","admin"))
    #cursor.execute("delete from usermaster")
    #cursor.execute("drop table Usermaster")
conn.commit()
app=Flask(__name__)
app.secret_key="123"

class User:
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password

users=[]

#users.append(User(id=2,username='raghul',password='raghul@123'))
#users.append(User(id=3,username='sasi',password='sasi@123'))
print(users)
@app.route("/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname=request.form['uname']
        upass = request.form['upass']
        cur.execute("select * from Usermaster")
        result=cur.fetchall()
        for row in result:
            print(row[1],row[2])
            users.append(User(id=row[0],username=str(row[1]),password=str(row[2])))

        print(users)
        for data in users:
            if data.username==uname and data.password==upass:
                session['userid']=data.id
                g.record=1
                return redirect(url_for('user'))
            else:
                g.record=0
        if g.record!=1:
            flash("Username or Password Mismatch...!!!",'danger')
            return redirect(url_for('login'))
    return render_template("login.html")
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    cur.execute("delete from usermaster where id=?",(item_id,))
    conn.commit()


    return redirect(url_for("usermaster"))
@app.before_request
def before_request():
    if 'userid' in session:
        for data in users:
            if data.id==session['userid']:
                g.user=data

@app.route('/user')
def user():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/usermaster',methods=['GET'])
def usermaster():
    cur.execute("select * from Usermaster")
    res=cur.fetchall()
    value=[]

    for row in res:
        value.append({"userid":str(row[0]),"name":str(row[1]),"email":str(row[3]),"role":str(row[4])})
    #value.append(dic)

    print(row)


    return render_template('usermaster.html',value=value)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
"""@app.route('/usermaster',methods=['POST'])
def adduser():
    if request.method=='POST':
        name=request.form.get('uname')
        password="abc@123"
        email=request.form.get('email')
        role=request.form.get('value')
        print(name,password,email,role)
        #return redirect(url_for('adduser'))

    return render_template('usermaster.html')"""
@app.route('/pushdata',methods=['POST','GET'])
def add_user1():
    global name
    data = request.json  # Expect JSON data
    name = data.get('username')
    password="abc@123"
    email = data.get('mail')
    role = data.get('role')  # Store popup data
    #msg=name,email,role
    #cursor.execute("select * from usermaster where username=?",name)
    #res=cursor.fetchone()
    #i=[]
    #for row in res:
     #   i.append(row[1])
    #print(i)
    if name in users:
        return jsonify({'status': 'Failure', 'data':'User Already Exist!!'})
    else:
        cur.execute("insert into usermaster(username,password,email,Role) values(?,?,?,?)",(name,password,email,role))
        conn.commit()



        return jsonify({'status': 'success', 'data': f"{name},{email},{role} added Successully"})


    #return redirect(url_for('usermaster'))
@app.route('/customer')
def customer():
    return render_template('customer_master.html')
@app.route('/shipment')
def shipment():
    return render_template('shipment_master.html')
@app.route('/mismaster')
def mismaster():
    return render_template('mismaster.html')
@app.route('/tracking')
def tracking():
    return render_template('tracking.html')
@app.route('/rate')
def rate():
    return render_template('Rate_Mater.html')
@app.route('/urg_ship',methods=['GET'])
def urg_ship():
    cur.execute("select * from shipping")
    res=cur.fetchall()
    value=[]

    for row in res:
        value.append({"tracking_no":str(row[0]),"shipping":str(row[1]),"destination":str(row[2])})
    #value.append(dic)
    print(value)
    #print(row)


    #return render_template('usermaster.html',value=value)
    return render_template('shipment_panel.html',value=value)
@app.route('/pushdata2',methods=['POST','GET'])
def pushdata2():
    global tracking_no
    data = request.json  # Expect JSON data
    tracking_no = data.get('tracking_no')
    shipping = data.get('shipping')
    destination = data.get('destination')  # Store popup data
    #msg=name,email,role
    """cur.execute("select * from shipping where tracking_no=?",(tracking_no,))
    res=cur.fetchone()
    i=[]
    for row in res:
       i.append({"tracking_id":str(row[0]),"shipping":str(row[1]),"destination":str(row[2])})
    """
    if tracking_no==1:
        return jsonify({'status': 'Failure', 'data':'User Already Exist!!'})
    else:
        cur.execute("insert into shipping(tracking_no,shipping,destination) values(?,?,?)",(tracking_no,shipping,destination))
        conn.commit()



        return jsonify({'status': 'success', 'data': f"{tracking_no},{shipping},{destination} added Successully"})

    pass
@app.route('/gnt_manifest')
def gnt_manifest():
    return render_template('gnt_manifest.html')
if __name__=='__main__':
        app.run(debug=True)
