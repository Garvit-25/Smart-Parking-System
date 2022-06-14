from flask import render_template, url_for, redirect,request, abort
from parkingSystemAutomation import app, cursor, bcrypt, db, client, GOOGLE_DISCOVERY_URL, GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID
from parkingSystemAutomation.forms import LoginForm,SignupForm,BookingForm
from flask_login import login_user, current_user, logout_user, login_required
from parkingSystemAutomation.models import User
import json
import requests
from functools import wraps

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        if request.form.get('google') == 'login':
            return redirect('login_google')
        elif request.form.get('user') == 'user_login':
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            query = 'Select * from User where email="'+str(form.email.data) + '\";'
            cursor.execute(query)
            user = cursor.fetchall()
            if user and bcrypt.check_password_hash(user[0][3], form.password.data):
                company = User(user[0][0], user[0][1], user[0][2], True)
                login_user(company)
                next_page = request.args.get('next')            
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
               return render_template('login.html',form=form)
        elif request.form.get('admin') == 'admin_login':
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            print('hello1')
            query = 'Select * from Company where company_email="'+str(form.email.data) + '\";'
            cursor.execute(query)
            user = cursor.fetchall()
            print(user)
            if user and bcrypt.check_password_hash(user[0][3], form.password.data):
                u = User(user[0][0], user[0][1], user[0][2], True, True)
                login_user(u)
                print('hello2')
                next_page = request.args.get('next')            
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
               return render_template('login.html',form=form)
    return render_template('login.html',form=form)

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('login'))

    form = SignupForm()
    # if request.method == 'POST':
    #     if request.form.get('action') == 'value':
    #         print("Hello")
    #     else:
    #         print("No")
    # else:
    #     print("bchxjdbsjakz")

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        #user = User(username=form.username.data, email=form.email.data, password=hashed_password, occupation=form.occupation.data)
        query = 'Insert into User (username,email,password) values("' + str(form.username.data) + '","' + str(form.email.data) + '","' +str(hashed_password) + '");'
        temp = cursor.execute(query)
        db.commit()
        return redirect(url_for('login'))
    return render_template('signup.html',form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/book',methods=['GET','POST'])
@login_required
def book():
    form = BookingForm()
    sql = "Select * from Location order by location;"
    cursor.execute(sql)
    choice = cursor.fetchall()
    form.location.choices = [(c[0],c[2]) for c in choice]
    if request.method == 'POST':
        if request.form.get('book_button') == 'book':
            # sql = 'Insert into Booking (location_id,id,slots,in_time,hours) values(' + str(form.location.data)
            print(form.location.choices)
            return redirect(url_for('index'))

    
    # print(form.location.choices)
    return render_template('book.html',form = form)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return f(*args, **kws)
            else:
                abort(405)
        else:
            abort(403)
    return decorated_function

@app.route('/createDatabase8967')
@admin_required
def createdb():
    create_table = """Create table User (
        id int(10) NOT NULL UNIQUE AUTO_INCREMENT,
        username varchar(60) NOT NULL, 
        email varchar(60) NOT NULL UNIQUE, 
        password varchar(256) , 
        PRIMARY KEY(id)
        );"""
    create_location_table = """Create table Location (
        location_id int(10) NOT NULL UNIQUE AUTO_INCREMENT, 
        company_id int(10) NOT NULL, 
        location varchar(256) NOT NULL UNIQUE, 
        PRIMARY KEY(location_id),
        FOREIGN KEY (company_id) REFERENCES Company (company_id)
        );"""

    create_company_table = """Create table Company (
        company_id int(10) NOT NULL UNIQUE AUTO_INCREMENT, 
        company_name varchar(60) NOT NULL UNIQUE,
        company_email varchar(60) NOT NULL UNIQUE, 
        password varchar(256) NOT NULL, 
        PRIMARY KEY(company_id)
        );"""
    create_parking_table = """Create table ParkingLot (
        id int(10) NOT NULL UNIQUE AUTO_INCREMENT, 
        level int(3) NOT NULL, 
        slot_no int(10) NOT NULL, 
        slot_area_name varchar(10) NOT NULL,
        in_time timestamp NOT NULL, 
        out_time timestamp NOT NULL, 
        location_id int(10) NOT NULL,
        PRIMARY KEY(id),
        FOREIGN KEY (location_id) REFERENCES Location (location_id)
        );"""

    create_booking_table = """Create Table Booking(
    booking_id int(10) NOT NULL UNIQUE AUTO_INCREMENT,
    location_id int(10) NOT NULL,
    id int(10) NOT NULL,
    slots int(2) NOT NULL,
    hours float(5,1) NOT NULL,
    in_time timestamp NOT NULL,
    PRIMARY KEY(booking_id),
    FOREIGN KEY (location_id) REFERENCES Location (location_id),
    FOREIGN KEY (id) REFERENCES User (id)
    ) """
    # cursor.execute(create_table)
    # cursor.execute(create_company_table)
    # cursor.execute(create_location_table)
    # cursor.execute(create_parking_table)
    #cursor.execute(create_booking_table)
    return redirect(url_for('signup'))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login_google")
def login_google():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login_google/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Doesn't exist? Add it to the database.
    query = 'Select * from User where email="'+users_email + '\";'
    cursor.execute(query)
    user = cursor.fetchall()
    if not user:
        query = 'Insert into User (username,email) values("' + users_name + '","' + users_email + '");'
        temp = cursor.execute(query)
        db.commit()
    query = 'Select * from User where email="'+users_email + '\";'
    cursor.execute(query)
    user = cursor.fetchall()
    u = User(user[0][0], user[0][1], user[0][2], True)
    # Begin user session by logging the user in
    login_user(u)

    # Send user back to homepage
    return redirect(url_for("index"))