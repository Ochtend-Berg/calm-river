# ------------------------------------------------------------------------------------------------------------------------------------------ #

from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

# -- NAME OF FLASK APP -- #
app = Flask(__name__)

# -- KEY TO INTERACT WITH FORMS -- #
app.config['SECRET_KEY'] = 'mijngeheimesleutel'

# -- 'C:\Users\Admin\Desktop\flask-sqlite\' -- #
basedir = os.path.abspath(os.path.dirname(__file__))  

# -- DATABASE SETTINGS TO CREATE A DATABASE INSTANCE -- #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -- CREATE DATABASE INSTANCE -- #
db = SQLAlchemy(app)

# -- MIGRATE DATABASE -- #
Migrate(app, db, os.path.join('database', 'migrations'))

# ------------------------------------------------------------------------------------------------------------------------------------------ #

# -- CREATE OBJECT LOGINMANAGER() -- #
login_manager = LoginManager()

# -- APP GETS FAMILIAR WITH LOGINMANAGER -- #
login_manager.init_app(app)

# -- SETS VIEW THAT IS RESPONSIBLE FOR LOGIN -- #
login_manager.login_view = "login"

# -- SETS MESSAGE WHEN USER IS NOT LOGGED IN-- #
login_manager.login_message = 'Je moet ingelogd zijn om deze pagina te bezoeken!'
login_manager.login_message_category = 'warning'

# ------------------------------------------------------------------------------------------------------------------------------------------ #

with app.app_context():

  # -- IMPORT MODELS -- #
  from models import User
  from models import Customer
  from models import Room_type
  from models import Room
  from models import Discount
  from models import Rate
  from models import Booking
  from models import Bookings_customer
  from models import Review

  db.create_all()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

