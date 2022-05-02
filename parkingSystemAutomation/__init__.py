from flask import Flask
from flask_material import Material
import pymysql
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
Material(app)
db = pymysql.connect(
        host= 'capstone.cnkzslk2pkyg.ap-south-1.rds.amazonaws.com', 
        port = 3306,
        user = 'admin', 
        password = '12345678',
        db = 'capstone',
        
        )

app.config['SECRET_KEY'] = '968331509722a24aaca4a6ab62dea0cd'
login_manager = LoginManager()
cursor = db.cursor()
bcrypt = Bcrypt(app)
login_manager.init_app(app)

from parkingSystemAutomation import routes