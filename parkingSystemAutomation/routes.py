from flask import render_template, url_for, redirect,request
from parkingSystemAutomation import app, cursor, bcrypt
from parkingSystemAutomation.forms import LoginForm,SignupForm
from flask_login import login_user, current_user, logout_user, login_required
from parkingSystemAutomation.models import Behnchod

@app.route('/')
@app.route('/index')
def index():
    # cursor.execute(create_table)
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # if request.method == 'POST':
    #     if request.form.get('action') == 'value':
    #         print("Hello")
    #     else:
    #         print("Fuck")
    # else:
    #     print("bchxjdbsjakz")

    if form.validate_on_submit():
        print("Hiii")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(hashed_password)
        query = 'Select * from User where username="'+str(form.username.data) + '\";'
        cursor.execute(query)
        user = cursor.fetchall()
        print(user[0][1])
        if user and bcrypt.check_password_hash(user[0][4], form.password.data):
            b = Behnchod(user[0][1], user[0][0], True)
            login_user(b)
            next_page = request.args.get('next')            
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
           return render_template('login.html',form=form)
        

    return render_template('login.html',form=form)

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    # if request.method == 'POST':
    #     if request.form.get('action') == 'value':
    #         print("Hello")
    #     else:
    #         print("Fuck")
    # else:
    #     print("bchxjdbsjakz")

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        #user = User(username=form.username.data, email=form.email.data, password=hashed_password, occupation=form.occupation.data)
        query = 'Insert into User (username,email,plate_number,password) values("' + str(form.username.data) + '","' + str(form.email.data) + '","' + str(form.license_plate_number.data) + '","' +str(hashed_password) + '");'
        print(query)
        cursor.execute(query)
        #flash('Your Account Has Been Successfully Created. Now you can Log In', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html',form = form)

@app.route('/login2/',methods=['GET','POST'])
def login2():
    print("maa ki chut")
    return render_template('index.html')

























@app.route('/createDatabase8967')
def createdb():
    # create_table = """Create table User (
    #     id int(10) NOT NULL UNIQUE AUTO_INCREMENT,
    #     username varchar(60) NOT NULL UNIQUE, 
    #     email varchar(60) NOT NULL UNIQUE, 
    #     plate_number varchar(10) NOT NULL UNIQUE, 
    #     password varchar(256) NOT NULL, 
    #     PRIMARY KEY(id)
    #     );"""
    # create_location_table = """Create table Location (
    #     location_id int(10) NOT NULL UNIQUE AUTO_INCREMENT, 
    #     company_id int(10) NOT NULL, 
    #     location varchar(256) NOT NULL UNIQUE, 
    #     PRIMARY KEY(location_id),
    #     FOREIGN KEY (company_id) REFERENCES Company (company_id)
    #     );"""

    # create_company_table = """Create table Company (
    #     company_id int(10) NOT NULL UNIQUE AUTO_INCREMENT, 
    #     company_name varchar(60) NOT NULL UNIQUE,
    #     company_email varchar(60) NOT NULL UNIQUE, 
    #     password varchar(256) NOT NULL, 
    #     PRIMARY KEY(company_id)
    #     );"""
    # create_parking_table = """Create table ParkingLot (
    #     id int(10) NOT NULL UNIQUE AUTO_INCREMENT, 
    #     level int(3) NOT NULL, 
    #     slot_no int(10) NOT NULL, 
    #     slot_area_name varchar(10) NOT NULL,
    #     in_time timestamp NOT NULL, 
    #     out_time timestamp NOT NULL, 
    #     location_id int(10) NOT NULL,
    #     PRIMARY KEY(id),
    #     FOREIGN KEY (location_id) REFERENCES Location (location_id)
    #     );"""
    #cursor.execute(create_table)
    # cursor.execute(create_company_table)
    # cursor.execute(create_location_table)
    # cursor.execute(create_parking_table)
    return redirect(url_for('login'))
