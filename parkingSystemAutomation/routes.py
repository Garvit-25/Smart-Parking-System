from flask import render_template, url_for, redirect,request
from parkingSystemAutomation import app, cursor, bcrypt, db, client, GOOGLE_DISCOVERY_URL, GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID
from parkingSystemAutomation.forms import LoginForm,SignupForm
from flask_login import login_user, current_user, logout_user, login_required
from parkingSystemAutomation.models import User
import json
import requests

# @app.route('/')
@app.route('/index')
def index():
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
    #         print("No")
    # else:
    #     print("bchxjdbsjakz")

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        query = 'Select * from User where username="'+str(form.username.data) + '\";'
        cursor.execute(query)
        user = cursor.fetchall()
        if user and bcrypt.check_password_hash(user[0][4], form.password.data):
            u = User(user[0][1], user[0][0], True)
            login_user(u)
            next_page = request.args.get('next')            
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
           return render_template('login.html',form=form)
    return render_template('login.html',form=form)

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
        query = 'Insert into User (username,email,plate_number,password) values("' + str(form.username.data) + '","' + str(form.email.data) + '","' + str(form.license_plate_number.data) + '","' +str(hashed_password) + '");'
        temp = cursor.execute(query)
        # print(temp)
        db.commit()
        #flash('Your Account Has Been Successfully Created. Now you can Log In', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html',form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index2'))

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
    # cursor.execute(create_table)
    # cursor.execute(create_company_table)
    # cursor.execute(create_location_table)
    # cursor.execute(create_parking_table)
    return redirect(url_for('login'))


# @app.route("/")
# def index2():
#     if current_user.is_authenticated:
#         return (
#             "<p>Hello, {}! You're logged in! Email: {}</p>"
#             "<div><p>Google Profile Picture:</p>"
#             '<a class="button" href="/logout">Logout</a>'.format(
#                 current_user.name, "dsjhdsjhdhs"
#             )
#         )
#     else:
#         return '<a class="button" href="/login2">Google Login</a>'

# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()

# @app.route("/login2")
# def login2():
#     # Find out what URL to hit for Google login
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]

#     # Use library to construct the request for Google login and provide
#     # scopes that let you retrieve user's profile from Google
#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)

# @app.route("/login2/callback")
# def callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get("code")

#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
#     token_url, headers, body = client.prepare_token_request(
#         token_endpoint,
#         authorization_response=request.url,
#         redirect_url=request.base_url,
#         code=code
#     )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )

#     # Parse the tokens!
#     client.parse_request_body_response(json.dumps(token_response.json()))
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)
#     if userinfo_response.json().get("email_verified"):
#         unique_id = userinfo_response.json()["sub"]
#         users_email = userinfo_response.json()["email"]
#         picture = userinfo_response.json()["picture"]
#         users_name = userinfo_response.json()["given_name"]
#     else:
#         return "User email not available or not verified by Google.", 400
#     user1 = User(users_name, 3, True)

#     # Doesn't exist? Add it to the database.
#     query = 'Select * from User where username="'+users_name + '\";'
#     cursor.execute(query)
#     user = cursor.fetchall()
#     if not user:
#         query = 'Insert into User (username,email,plate_number,password) values("' + users_name + '","' + users_email + '","' + "212122" + '","' +"21212312121212" + '");'
#         temp = cursor.execute(query)
#         # print(temp)
#         db.commit()
#     # Begin user session by logging the user in
#     login_user(user1)

#     # Send user back to homepage
#     return redirect(url_for("index2"))