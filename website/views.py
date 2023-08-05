from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Quote, User
import urllib.request, json
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get("text")
        author = request.form.get("author")

        user_id = User.get_id(current_user)

        quote_insert = Quote(text=text, author=author, user_id=user_id)
        db.session.add(quote_insert)
        db.session.commit()

        flash('Quote added to favourites!', category='success')
        return redirect(url_for('views.index'))

    else:
        url = "https://stoic-quotes.com/api/quote"
        # get response data (stoic quote from above url)
        response = urllib.request.urlopen(url)
        data = response.read()
        # convert json data to python dict
        dict = json.loads(data)

        return render_template('index.html', result = dict)

@views.route('/favourites', methods=['GET', 'POST'])
@login_required
def favourites():
    if request.method == 'POST':
        id = request.form.get("id")
        if id:           
            quote = Quote.query.filter_by(id=id).one()
            db.session.delete(quote)
            db.session.commit()

            flash('Quote deleted from favourites!', category='success')
            return redirect(url_for('views.favourites'))
        else:
            flash('No quote found.', category='error')

    else:
        quotes = Quote.query

        return render_template('favourites.html', quotes = quotes)

@views.route('/get_quotes')
def get_quotes():
    url = "https://stoic-quotes.com/api/quotes"
    # get response data (stoic quote from above url)
    response = urllib.request.urlopen(url)
    data = response.read()
    # convert json data to python dict
    quotes = json.loads(data)

    return render_template('quotes_table.html', quotes = quotes)

