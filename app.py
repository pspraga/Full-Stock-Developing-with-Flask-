from flask import Flask,render_template,request,session,redirect,url_for,g,flash,jsonify
from database import init_db
import sqlite3
conn=sqlite3.connect("Mydb.db",check_same_thread=False)
cur=conn.cursor()

app=Flask(__name__)
app.secret_key="123"

class User:
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password

users=[]
cur.execute("select * from Usermaster")
result=cur.fetchall()
for row in result:
    print(row[1],row[2])
    users.append(User(id=row[0],username=str(row[1]),password=str(row[2])))
#users.append(User(id=2,username='raghul',password='raghul@123'))
#users.append(User(id=3,username='sasi',password='sasi@123'))
print(users)
@app.route("/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname=request.form['uname']
        upass = request.form['upass']
        
        #print(users)
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
@app.route('/usermaster')
def usermaster():
    return render_template('usermaster.html')
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
    msg=''
    data = request.json  # Expect JSON data
    name = data.get('username')
    email = data.get('mail')
    role = data.get('role')  # Store popup data
    msg=name,email,role
    return jsonify({'status': 'success', 'data': (name,email,role)})
    #return redirect(url_for('usermaster'))

if __name__=='__main__':
    init_db()
    app.run(debug=True)