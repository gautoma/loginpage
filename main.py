from flask import Flask, render_template, request
#from flask.wrappers import Request
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="password", database="sample",\
                                auth_plugin="mysql_native_password")

cursor = mydb.cursor(buffered=True)                

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['post','get'])
def register():
    error=None
    success=None
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        if len(firstname) < 2: 
            error = "Firstname is too short"
        elif len(password) < 6:
            error = "Password is too short"
        elif password != confirmpassword:
            error = "Passwords do not match"
        else:
            query = "INSERT INTO users(id,firstname,lastname,email,password,date) VALUES (NULL, %s, %s, %s, %s, NOW())"
            cursor.execute(query, (firstname,lastname,email,password))
            mydb.commit()
            success = "You account has been created"

    return render_template('register.html',error=error,msg=success)


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password = request.form.get('password')
    cursor.execute("""SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}'"""
                   .format(email,password))
    users = cursor.fetchall()
    if len(users)>0:
        return render_template('home.html')
    else:
        return render_template('login.html')
    #return users

   # return "The email is {} and password is {}".format(email,password)




if __name__ == "__main__":
    app.run(debug=True)

