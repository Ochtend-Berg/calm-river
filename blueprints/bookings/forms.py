@app.route('/bookings/index')
def bookings_index():
    return render_template('bookings/reviews_index.html')


@app.route('/bookings/show')
def bookings_show():
    return render_template('bookings/show.html')


@app.route('/bookings/edit')
def bookings_edit():
    return render_template('bookings/edit.html')