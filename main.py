from flask import Flask, render_template, request, redirect, url_for, session,flash
import re
from datetime import datetime
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account={"username":username,"password":password}
        f = open("DB.txt", "r")
        dem=0
        id=0
        for x in f:
            dem+=1
            arr= x.split(";")
            if arr[0]==username and arr[1]==password:
                id=dem
                account['id']=id
                account['email']=arr[2]
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html',title="Login")
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = {}
        f = open("DB.txt", "r")
        for x in f:
            arr = x.split(";")
            if arr[0] == username and arr[1] == password:
                account = {"username": username, "password": password}
        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
            file1 = open("DB.txt", "a")
            file1.write(f'{username};{password};{email}\n')

            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        flash("Please fill out the form!", "danger")
    return render_template('auth/register.html',title="Register")
@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        return render_template('home/home.html', username=session['username'],title="Home")
    return redirect(url_for('home'))


@app.route('/feedback', methods = ['POST'])
def feedback():
    feedback = request.form['feedback']
    username = request.form['username']
    time =datetime.now()
    file1 = open("feedback.txt", "a")
    print(feedback)
    file1.write(f'{username};{feedback};{time}\n')
    return render_template('auth/feedback.html')

if __name__ =='__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(port=5001)