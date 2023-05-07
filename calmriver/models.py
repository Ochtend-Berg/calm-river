# ------------------------------------------------------------------------------------------------------------------------------------------ #

from calmriver import app, db, login_manager
from calmriver.imports import *
from datetime import datetime

# ------------------------------------------------------------------------------------------------------------------------------------------ #

with app.app_context():

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    # GETS CURRENT LOGIN-IN USER ID
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class User(db.Model, UserMixin):

        # -- TABLE NAME : DEFAULT 'User'-- #
        __tablename__ = 'users'

        # -- TABLE COLUMNS -- #
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(64), unique=True, index=True)
        username = db.Column(db.String(64), unique=True, index=True)
        password_hash = db.Column(db.String(128))

        # -- CONSTRUCTOR -- #
        def __init__(self, email, username, password):
            self.email = email
            self.username = username
            self.password_hash = generate_password_hash(password)

        # -- CHECKS USER PASSWORD -- #
        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class Customer(db.Model, UserMixin):
        __tablename__ = 'customers'

        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(64), index=True)
        last_name = db.Column(db.String(64), index=True)
        email = db.Column(db.String(128))
        created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

        def __init__(self, first_name, last_name, email):
            self.first_name = first_name
            self.last_name = last_name
            self.email = email

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class Room_type(db.Model):
        __tablename__ = 'room_types'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), index=True)
        slug = db.Column(db.String(255), index=True)
        max_persons = db.Column(db.Integer, index=True)
        bed_persons = db.Column(db.Integer, index=True)
        has_bath = db.Column(db.Integer, index=True)
        has_wifi = db.Column(db.Integer, index=True)
        price = db.Column(db.Float, index=True)
        description = db.Column(db.Text, index=True)
        created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

        def __init__(self, name, slug, max_persons, bed_persons, has_bath, has_wifi, price, description):
            self.name = name
            self.slug = slug
            self.max_persons = max_persons
            self.bed_persons = bed_persons
            self.has_bath = has_bath
            self.has_wifi = has_wifi
            self.price = price
            self.description = description

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class Room(db.Model):
        __tablename__ = 'rooms'

        id = db.Column(db.Integer, primary_key=True)
        number = db.Column(db.Integer, unique=True, index=True)
        room_type_id = db.Column(db.Integer, db.ForeignKey('room_types.id'), index=True)
        created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

        def __init__(self, number, room_type_id):
            self.number = number
            self.room_type_id = room_type_id

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class Discount(db.Model):
        __tablename__ = 'discounts'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), index=True)
        code = db.Column(db.String(50), index=True)
        discount = db.Column(db.Integer, index=True)
        created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

        def __init__(self, name, code, discount):
            self.name = name
            self.code = code
            self.discount = discount

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class Rate(db.Model):
        __tablename__ = 'rates'
        __table_args__ = (
            db.UniqueConstraint('room_type_id', 'is_weekend', name='unique_room_constraint'),
        )

        id = db.Column(db.Integer, primary_key=True)
        value = db.Column(db.Integer, index=True)
        room_type_id = db.Column(db.Integer, db.ForeignKey('room_types.id'))
        is_weekend = db.Column(db.Boolean())
        created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

        def __init__(self, value, room_type_id, is_weekend):
            self.value = value
            self.room_type_id = room_type_id
            self.is_weekend = is_weekend

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class Booking(db.Model):
        __tablename__ = 'bookings'

        id = db.Column(db.Integer, primary_key=True)
        room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), index=True)
        start = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        end = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        is_reservation = db.Column(db.Boolean(), default=False, index=True)
        is_paid = db.Column(db.Boolean(), default=False, index=True)
        notes = db.Column(db.Text, nullable=True, index=True)
        order_number = db.Column(db.Integer, index=True)

        created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

        def __init__(self, room_id, start, end, is_reservation, is_paid, notes, order_number):
            self.room_id = room_id
            self.start = start
            self.end = end
            self.is_reservation = is_reservation
            self.is_paid = is_paid
            self.notes = notes
            self.order_number = order_number

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class Bookings_customer(db.Model):
        # INTERACTION TABLE BETWEEN BOOKINGS AND CUSTOMERS
        __tablename__ = 'bookings_customers'

        id = db.Column(db.Integer, primary_key=True)
        booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), index=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
        customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), index=True)

        created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

        def __init__(self, booking_id, user_id, customer_id):
            self.booking_id = booking_id
            self.user_id = user_id
            self.customer_id = customer_id

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class Rating(db.Model):
        # INTERACTION TABLE BETWEEN BOOKINGS AND CUSTOMERS
        __tablename__ = 'ratings'

        id = db.Column(db.Integer, primary_key=True)
        rating = db.Column(db.String(50), index=True)

        created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

        def __init__(self, rating):
            self.rating = rating

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    class Review(db.Model):
        # INTERACTION TABLE BETWEEN BOOKINGS AND CUSTOMERS
        __tablename__ = 'reviews'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), index=True)
        rating_id = db.Column(db.Integer, db.ForeignKey('ratings.id'), default=5, index=True)
        email = db.Column(db.String(255))
        comment = db.Column(db.Text, nullable=True)

        created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

        def __init__(self, name, rating_id, email, comment):
            self.name = name
            self.rating_id = rating_id
            self.email = email
            self.comment = comment

    # -------------------------------------------------------------------------------------------------------------------------------------- #

    db.create_all()

    # -------------------------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------------------------------------------------ #

