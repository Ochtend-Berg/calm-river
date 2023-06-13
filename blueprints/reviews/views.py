from app import app, db
from imports import *
from models.Review import Review
from flask import session
from forms import ReviewForm

# -- BLUEPRINT('NAME OF BLUEPRINT, NAME OF APPLICATION, FOLDER CONTAINING LOGIC) -- #
reviews_bp = Blueprint('reviews_bp', __name__, template_folder='templates')


@reviews_bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    active_page = 'reviews'
    session["url"] = active_page
    reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    form = ReviewForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        rating_id = form.rating_id.data
        comment = form.comment.data

        try:
            review = Review(name=name, email=email, rating_id=rating_id, comment=comment)
            db.session.add(review)
            db.session.commit()
            flash('Dank voor uw recensie.', 'success')
            return redirect(url_for('reviews_bp.reviews'))

        except ValueError:
            db.session.rollback()
            flash('Er is iets misgegaan. Probeer het opnieuw!', 'danger')

    return render_template('reviews_index.html', form=form, reviews=reviews, active_page=active_page)
