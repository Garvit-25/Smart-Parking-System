from flask import Flask
from flask_material import Material
import pymysql
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)
Material(app)
db = pymysql.connect(
        host= YOUR_ENDPONT, 
        port = PORT,
        user = USERNAME, 
        password = PASSWORD,
        db = DB_NAME,
        )

app.config['SECRET_KEY'] = SECRET_KEY
GOOGLE_CLIENT_ID = CLIENT_ID
GOOGLE_CLIENT_SECRET = CLIENT_SECRET
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)
login_manager = LoginManager()
cursor = db.cursor()
bcrypt = Bcrypt(app)
login_manager.init_app(app)

from parkingSystemAutomation import routes
