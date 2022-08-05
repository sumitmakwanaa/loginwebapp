from flask import Flask, redirect, url_for, request, session, render_template
import sqlite3
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '930864c7dc75f4'
app.config['MAIL_PASSWORD'] = '1f89bec013cbfd'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

s = URLSafeTimedSerializer('123')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/register')
def register():
    return render_template('register.html', title = 'Register')

@app.route('/login')
def login():
    return render_template('login.html', title = 'Login')
    
@app.route('/cemail')
def cemail():
    return render_template('cemail.html', title = 'Confirm email')
    
@app.route('/confirm_email', methods=['POST'])
def confirm_email():
    if request.method == 'POST':
        email = request.form['email']
        token = s.dumps(email, salt = 'email-confirm')

        msg = Message('Confirm email', sender = 'sumitmakwanaa@gmail.com', recipients = [email])

        link = url_for('home', token = token, _external = True)

        msg.body = 'your link is {}'.format(link)

        mail.send(msg)

        return render_template('afcdcemail.html', email = email, token = token, title = 'Confirm-email')

@app.route('/confirmemail/<token>')
def confirmemail(token):
    try:
        email = s.loads(token, salt = 'email-confirm', max_age = 500)
    except SignatureExpired:
        return '<h1>The token is expired</h1>'
    return render_template('home.html')

@app.route('/insertdata', methods=['POST'])
def insertdata():
    if (request.method == 'POST'):
        if  request.form['username']!="" and request.form['password'] != "":
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            conn = sqlite3.connect('site.db')
            c = conn.cursor()
            c.execute("INSERT INTO users VALUES('"+username+"','"+email+"', '"+password+"')")
            msg = "Register successfully"
            conn.commit()
            conn.close()
            return render_template('login.html', title = 'login') 
        else:
            msg = "Register failed"
            return render_template('register.html', title = 'Register', msg=msg)

@app.route('/validatedata', methods=['POST'])
def validatedata():
    if (request.method == 'POST'):
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect('site.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = '"+email+"' and password = '"+password+"'")
        i = c.fetchone()
        if i and email == i[1] and password == i[2]:
            session["Loged in"] = True
            session["email"] = email
            msg = "Login successfully"
            return render_template('home.html',title = 'Home', msg = msg)
        else:
            msg = "Couldn't login'"
            return render_template('login.html', title = 'Login',msg=msg)  
    else:
        return "Please enter valid username and password" 


if __name__ == '__main__':
    app.run(debug = True)