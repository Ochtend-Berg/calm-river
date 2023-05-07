# ------------------------------------------------------------------------------------------------------------------------------------------ #

from calmriver.imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

# pip install flask_login
# pip install email_validator

# -- NAME OF FLASK APP -- #
app = Flask(__name__)

# -- KEY TO INTERACT WITH FORMS -- #
app.config['SECRET_KEY'] = 'mijngeheimesleutel'

# -- 'C:\Users\Admin\Desktop\flask-sqlite\' -- #
basedir = os.path.abspath(os.path.dirname(__file__))  

# -- DATABASE SETTINGS TO CREATE A DATABASE INSTANCE -- #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -- CREATE DATABASE INSTANCE -- #
db = SQLAlchemy(app)

# -- MIGRATE DATABASE -- #
Migrate(app, db)

# ------------------------------------------------------------------------------------------------------------------------------------------ #

# -- CREATE OBJECT LOGINMANAGER() -- #
login_manager = LoginManager()

# -- APP GETS FAMILIAR WITH LOGINMANAGER -- #
login_manager.init_app(app)

# -- SETS VIEW THAT IS RESPONSIBLE FOR LOGIN -- #
login_manager.login_view = "login"

# ------------------------------------------------------------------------------------------------------------------------------------------ #

