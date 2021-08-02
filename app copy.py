# Store this code in 'app.py' file
from MySQLdb import connections
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'foodapp'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
     
        
		if account:
           
      
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)

        
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)
@app.route('/login', methods =['GET', 'POST'])


@app.route('/logout')
def logout():
 session.pop('loggedin', None)
 session.pop('id', None)
 session.pop('username', None)
 return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		organisation = request.form['organisation']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']	
		postalcode = request.form['postalcode']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO accounts(username,password,email,organisation,address,city,state,country,postalcode) VALUES ( % s, % s, % s, % s, % s, % s, % s, % s, % s)', (username, password, email, organisation, address, city, state, country, postalcode, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		
		return render_template("index.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()	
		return render_template("display.html", account = account)
	return redirect(url_for('login'))

@app.route("/update", methods =['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			organisation = request.form['organisation']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			country = request.form['country']	
			postalcode = request.form['postalcode']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor.execute('UPDATE accounts SET username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg = msg)
	return redirect(url_for('login'))

#ADMIN OPERATION
@app.route("/adminmenu",methods=["GET","POST"])
def adminmenu():
    if 'loggedin' in session and request.method=="GET":
        #idd=request.args.get('FID')
       
        #print(idd)
       
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from menu")
        data=cursor.fetchall()
        
        #for i in data:
            #print(i)
            
           
             
            #if idd == i['FOODID']:
                #print("Deleted")
               # msg='deleted'
                #return render_template("menu.html",msg=msg)
            
            #if i['FOODID']==id:
                #print("YES")
                #cursor.execute('delete from menu where FOODID== %s',(id,))
                #ursor.close()
                
            #else:
                #msg="No FOOD PRESENT"
               
        return render_template("adminmenu.html",data=data)   
#admin operation     
@app.route('/del',methods=["GET","POST"])
def ndel():
    if 'loggedin' in session:
        print(session['id'])
        id=request.args.get('FID')
        #print(type(id))
        z=id
        print(z)
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select*from menu")
        data=cursor.fetchall()
        cursor.close()
        for i in data:
            print(i)
            if str(i['FOODID']) == request.args.get('FID'):
                print("yes")
                cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("delete  from menu where FOODID = %s",(id))
                query="delete from menu where FOODID = %s"
                val=(id,)
                cursor.execute(query,val)
                mysql.connection.commit()
                cursor.fetchone
                print("Successful")
            else:
                print('unsuccesful')
    return redirect(url_for('adminmenu'))
#adminoperation       
@app.route('/updatefood',methods=["GET","POST"])
def updatefood():
    if 'loggedin' in session:
        idd=request.args.get('FOOID')
        
        if request.method=="GET":
            idd=request.args.get('FOOID')
            print(idd)
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from menu where FOODID=%s",(idd,))
            data=cursor.fetchall()
            return render_template('upfood.html',data=data)
        else:
            if request.method=='POST' and "foodname" in request.form and "foodtype" in request.form and "price" in request.form:
                foodname=request.form["foodname"]
                print(foodname)
                
                foodtype=request.form["foodtype"]
                price=request.form["price"]
                cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query="update menu set FOODNAME=%s, FOODTYPE=%s , Price=%s  where FOODID=%s"
                val=(foodname,foodtype,price,idd)
                cursor.execute(query,val)
                #cursor.execute("update menu set FOODNAME=%s  FOODTYPE=%s and Price=%s  where FOODID=%s",(foodname,foodtype,price,idd))
                mysql.connection.commit()
                cursor.close()
                print("successful")
                return redirect(url_for('adminmenu'))
            
            else:
                print("unsuceessful")
                return render_template('upfood.html')
        
       
    return redirect(url_for('menu'))


#admin
@app.route("/adminadd",methods=["GET","POST"])
def adminadd():

    
    if request.method=='POST' and 'FoodName' in request.form and 'FoodId' in request.form and 'FoodType' in request.form and 'Price' in request.form:
        FoodID=request.form['FoodId']
        FoodName=request.form['FoodName']
        FoodType=request.form['FoodType']
        Price=request.form['Price']

        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into menu values(%s,%s,%s,%s)",( FoodID, FoodName, FoodType,Price))
        mysql.connection.commit()
        cursor.close()
        msg="Inserted Successfully"
    else:
        msg="Unsuccessful"
        
    
       
    return render_template("adminadd.html",msg=msg)
     
@app.route("/type",methods=["GET","POST"])
def type():
     s="Veg"
     k="Non-Veg"
     cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     query=("select*from menu where FOODTYPE = %s")
     val=(s,)
     cursor.execute(query,val)
     data=cursor.fetchall()
     query=("select* from menu where FOODTYPE=%s")
     val=(k,)
     cursor.execute(query,val)
     ndata=cursor.fetchall()
     return render_template("type.html",data=data,ndata=ndata)
@app.route("/orders")
def infoorders():
    cid=session['id']
   
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from menu")
    menu=cursor.fetchall()
   
    cursor.execute("select * from orders where CustomerID=%s",(cid,))
    sdata=cursor.fetchall()
  
    cursor.execute("select sum(Price) from orders where CustomerID=%s",(cid,))
    total=cursor.fetchone()
  
    cursor.close()
    return render_template("orders.html",sdata=sdata,menu=menu,total=total)
    
@app.route("/men",methods=["GET","POST"])    
def placeorders():
    
    
    
    
    try:
      
  
  
        #if request.method=='POST'and 'orders' in request.form:
            ord= request.args.get('FID')
            print(ord)
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query=("select*from menu where FOODID = %s")
            val=(ord,)
            cursor.execute(query,val)
            
            data= cursor.fetchone()
            rec=data
            cid=session['id']
            print(cid)
           


            cursor.execute("insert into orders values(%s,%s,%s,%s,%s)",(rec["FOODID"],rec["FOODNAME"],rec["FOODTYPE"],rec["Price"],cid))
            mysql.connection.commit()
            
            #msg="inserted "
            
            
            
            cursor.execute("select sum(Price) from orders where CustomerID = %s",(cid,))
           
           
            if cursor.rowcount==0:
                msg="No order present,Value==0"
            else:
            	total=cursor.fetchone()
            cursor.close()
            return redirect(url_for('menu'))
    except:
        return "Errror"
    #return redirect(url_for('menu.html'))
  
@app.route("/deleteorders",methods=["GET","POST"])  
def delorder():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #cursor.execute("select*from orders")
    #data=cursor.fetchall()
    
    delete=request.args.get('FID')
    cursor.execute("delete from orders where FOODID=%s",(delete,))
    mysql.connection.commit()
    cursor.fetchone()
    cursor.close()
       
  
    return redirect(url_for('infoorders'))

@app.route("/deletemenuitem",methods=["GET","POST"])
def delmenu():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select*from menu")
    data=cursor.fetchall()
    if request.method=="POST"and "delete" in request.form:
        delete=request.form["delete"]
        cursor.execute("delete from menu where FOODID=%s",(delete,))
        mysql.connection.commit()
        cursor.close()
        msg="Deleted successfully"
    else:
        msg="Error occured/ Data is not present"
    return render_template("delmenu.html",data=data,msg=msg)
#ADMIN CODE
@app.route('/alogin', methods =['GET', 'POST'])
def alogin():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM admin_accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
     
        
		if account:
           
      
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('adminindex.html', msg = msg)

        
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route("/adminindex")
def adminindex():
	if 'loggedin' in session:
		
		return render_template("adminindex.html")
	return redirect(url_for('login'))

@app.route('/adminorders',methods=['GET','POST'])
def adminorders():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select accounts.id CustomerID,accounts.username CustomerName,orders.FOODID FOODID,orders.FOODNAME FOODNAME,orders.FOODTYPE FOODTYPE,orders.Price PRICE from accounts inner join orders on accounts.id=orders.CustomerID;')
    data=cursor.fetchall()
    print(data)
    return render_template('adminorders.html',data=data)
        
	 
@app.route("/menu",methods=["GET","POST"])
def menu():
    if 'loggedin' in session and request.method=="GET":
        #idd=request.args.get('FID')
       
        #print(idd)
       
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from menu")
        data=cursor.fetchall()
      
        #for i in data:
            #print(i)
            
           
             
            #if idd == i['FOODID']:
                #print("Deleted")
               # msg='deleted'
                #return render_template("menu.html",msg=msg)
            
            #if i['FOODID']==id:
                #print("YES")
                #cursor.execute('delete from menu where FOODID== %s',(id,))
                #ursor.close()
                
            #else:
                #msg="No FOOD PRESENT"
               
        return render_template("menu.html",data=data)             


if __name__ == "__main__":
	app.run(host ="localhost", port = int("5002"),debug=True)
