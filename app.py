# Flask imports
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import forms
import organizationCodes

# Setup
app = Flask(__name__)
login = LoginManager(app)
db = SQLAlchemy(app)


# Config
app.config['SECRET_KEY'] = 'abcdefghijklmnopqrstuvwxyz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

login.login_view = 'login'


# Databases
class accounts(UserMixin, db.Model):
    id = db.Column('account_id', db.Integer, primary_key=True)
    firstName = db.Column(db.String(32))
    lastName = db.Column(db.String(32))
    username = db.Column(db.String(16))
    password = db.Column(db.String(32))
    org_code = db.Column(db.String(8))

    def __init__(self, firstName, lastName, username, password, org_code):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = password
        self.org_code = org_code


class organizations(db.Model):
    id = db.Column('org_id', db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    code = db.Column(db.String(8))
    email = db.Column(db.String(128))

    def __init__(self, name, code, email):
        self.name = name
        self.code = code
        self.email = email


db.create_all()


@login.user_loader
def load_account(uuid):
    return accounts.query.get(int(uuid))


# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.signupForm()
    if form.validate_on_submit():
        account = accounts(request.form['firstName'],
                           request.form['lastName'],
                           request.form['username'],
                           generate_password_hash(request.form['password']),
                           request.form['org_code'])
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.loginForm()
    if form.validate_on_submit():
        account = accounts.query.filter_by(username=request.form['username']).first()
        if account and check_password_hash(account.password, form.password.data):
            print("Sign-in Attempted: Access Granted")
            session['username'] = account.username
            login_user(account)
            return redirect(url_for('dashboard'))
        else:
            print("Sign-in Attempted: Access Denied")
            flash("Incorrect Login Parameters.")
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.registerForm()

    # Generate the Random Organization Code for the user to accept when POSTed

    if form.validate_on_submit():
        code = organizationCodes.generateCode()
        print(code)
        organization = organizations(request.form['name'],
                                     code,
                                     request.form['email'])
        db.session.add(organization)
        db.session.commit()
        return redirect(url_for('signup'))
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    username = (session['username'])

    return render_template('dashboard.html', username=username)
