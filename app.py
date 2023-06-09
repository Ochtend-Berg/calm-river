# ------------------------------------------------------------------------------------------------------------------------------------------ #

from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

# -- NAME OF FLASK APP -- #
app = Flask(__name__)

# -- KEY TO INTERACT WITH FORMS -- #
app.config['SECRET_KEY'] = 'mijngeheimesleutel'

# Flask-mail configuratie
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'ad7dbc80d47d4c'
app.config['MAIL_PASSWORD'] = '5162580613de17'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'hotelcalmriver@info.com'

# -- 'C:\Users\Admin\Desktop\flask-sqlite\' -- #
basedir = os.path.abspath(os.path.dirname(__file__))

# -- DATABASE SETTINGS TO CREATE A DATABASE INSTANCE -- #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)

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
login_manager.login_view = "auth_bp.login"

# -- SETS MESSAGE WHEN USER IS NOT LOGGED IN-- #
login_manager.login_message = 'Je moet ingelogd zijn om deze pagina te bezoeken!'
login_manager.login_message_category = 'warning'

# -- IMPORT BLUEPRINTS -- #
from blueprints.auth.views import auth_bp
from blueprints.basic.views import basic_bp
from blueprints.bookings.views import bookings_bp
from blueprints.profile.views import profile_bp
from blueprints.reviews.views import reviews_bp
from blueprints.rooms.views import rooms_bp

# -- REGISTER BLUEPRINTS -- #
app.register_blueprint(auth_bp)
app.register_blueprint(basic_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(rooms_bp, url_prefix="/rooms")

if __name__ == '__main__':
    app.run(debug=True)
