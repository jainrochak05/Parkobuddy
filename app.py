from flask import *
import mysql.connector
import random
import smtplib
from email.message import EmailMessage

server = smtplib.SMTP('smtp.office365.com',587)
server.starttls()
server.login('rochak.jain@outlook.com','Rochak@2005')

rid=random.randint(10000,99999)


mydb = mysql.connector.connect(
  host="b4dfmejxwmiwx5wwrnyq-mysql.services.clever-cloud.com",port="3306",
  user="uvd345a067tohlfz",
  password="7tRMR7rdmDT1nRwYJgRX",database="b4dfmejxwmiwx5wwrnyq"
)
cur=mydb.cursor()
app = Flask(__name__)
app.secret_key = "abc"
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        password = userDetails['pass']
        email= userDetails['email']
        a="This is your unique id which u will require to login into parkobuddy app\nUNIQUE ID:"+str(rid)
        msg=EmailMessage()
        msg['subject'] = "Unique ID"
        msg['from'] = "rochak.jain@outlook.com"
        msg['to'] = email
        msg.set_content(a)
        server.send_message(msg)
        cur.execute("INSERT INTO users(u_id ,username, password) VALUES(%s, %s ,%s)",(rid,name, password))
        mydb.commit()
    return render_template('login.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get("nm")
        password = request.form.get('pass')
        uid= int(request.form.get("uid"))
        h=uid
        p=(uid ,name, password)
        run = "select * from users"
        cur.execute(run)
        data  = cur.fetchall()
        usr=[]
        for i in data:
            usr.append(i)
        if p in usr:
            run = "select username from users where u_id = '{}'".format(uid)
            cur.execute(run)
            data  = cur.fetchall()
            ur=[]
            for i in data:
                ur.append(i)
            x=""
            for l in ur:
                for g in l:
                    x=x+g
            return render_template("user.html",d=x,uid=uid)
        else:
            return "bad password"
 
    return render_template('login.html')


    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        userDetails = request.form
        r = userDetails['reg']
        if r=="centd":
            o="Central Delhi"
            headings = ("Address (Central Delhi)","Total Space", "Occupied")
            while True:
                run = "select Location , total , inuse from centd"
                cur.execute(run)
                data  = cur.fetchall()
                while True:
                    return render_template("data.html",headings=headings,data=data,ar=o)
        if r=="od":
            o="Old Delhi"
            headings = ("Address (Old Delhi)","Total Space", "Occupied")
            run = "select Location , total , inuse from od"
            cur.execute(run)
            data  = cur.fetchall()
            return render_template("data.html",headings=headings,data=data,ar=o)
        if r=="sd":
            o="South Delhi"
            headings = ("Address (South Delhi)","Total Space", "Occupied")
            run = "select Location , total , inuse from sd"
            cur.execute(run)
            data  = cur.fetchall()
            return render_template("data.html",headings=headings,data=data,ar=o,rr=r)
    return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    t=""
    if request.method == 'POST':
        userDetails = request.form
        r = userDetails['reg']
        usid=userDetails['uid']
        t=t+usid
        headings = ("Address","Total Space", "Occupied" , "Vacant", "Parking ID")
        if r=="centd":
            f="Central Delhi"
            cur.execute("select Location , total , inuse , total-inuse as Vacant , p_id from centd where own_id ={}".format(usid,))
            data=cur.fetchall()
            return render_template("data2.html",headings=headings,data=data,ar=f)
        if r=="od":
            f="Old Delhi"
            cur.execute("select Location , total , inuse , total-inuse as Vacant , p_id from od where own_id ={}".format(usid,))
            data=cur.fetchall()
            return render_template("data2.html",headings=headings,data=data,ar=f)
        if r=="sd":
            f="South Delhi"
            cur.execute("select Location , total , inuse , total-inuse as Vacant , p_id from sd where own_id ={}".format(usid,))
            data=cur.fetchall()
            return render_template("data2.html",headings=headings,data=data,ar=f)
    return render_template('user.html')

@app.route('/new', methods=['GET', 'POST'])
def add():
    cur1=mydb.cursor()
    if request.method == 'POST':
        a=request.form
        uid=a.get('ud')
        loc=a.get('loc')
        tc=a.get('tc')
        r=a.get('reg')
        inu=0
        l=random.randint(1000,9999)
        if r=="centd":
            cur1.execute("insert into centd values(%s,%s,%s,%s,%s)",(loc,tc,inu,uid,l))
            mydb.commit()
            return render_template('success.html')
            
        if r=="od":
            cur1.execute("insert into od values(%s,%s,%s,%s,%s)",(loc,tc,inu,uid,l))
            mydb.commit()
            return render_template('success.html')
            
        if r=="sd":
            cur1.execute("insert into sd values(%s,%s,%s,%s,%s)",(loc,tc,inu,uid,l))
            mydb.commit()  
            return render_template('success.html')
        cur1.close()
    return render_template("add-new.html")

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    cur2=mydb.cursor()
    if request.method == 'POST':
        a=request.form
        loc=a.get('pic')
        r=a.get('reg')
        if r=="centd":
            cur2.execute("delete from centd where p_id = %s",(loc,))
            mydb.commit()
            return render_template('success1.html')     
        if r=="od":
            cur2.execute("delete from od where p_id = %s",(loc,))
            mydb.commit()
            return render_template('success1.html')
        if r=="sd":
            run ="DELETE from sd where p_id = %s"
            a=(loc,)
            cur2.execute(run,a)
            mydb.commit()  
            return render_template('success1.html')
        cur2.close()
    return render_template("remove.html")

               
if __name__ == '__main__':    
    app.run(debug=True,host='0.0.0.0')