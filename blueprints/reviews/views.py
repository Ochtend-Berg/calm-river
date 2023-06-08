from main import app, db
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
        name = request.form['name']
        email = request.form['email']
        rating_id = request.form['rating_id']
        comment = request.form['comment']

        try:
            review = Review(name=name, email=email, rating_id=rating_id, comment=comment)
        except:
            flash('Er is iets misgegaan. Probeer het opnieuw!', 'danger')
            return redirect(url_for('reviews_bp.reviews'), code=302)

        db.session.add(review)
        db.session.commit()

        flash('Dank voor uw recensie.', 'success')

        return redirect(url_for('reviews_bp.reviews'))

    return render_template('reviews_index.html', form=form, reviews=reviews, active_page=active_page)



