from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import urllib.request, json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass

    else:
        url = "https://stoic-quotes.com/api/quote"
        # get response data (stoic quote from above url)
        response = urllib.request.urlopen(url)
        data = response.read()
        # convert json data to python dict
        dict = json.loads(data)

        return render_template('index.html', result = dict)

@views.route('/favourites')
@login_required
def favourites():
    return render_template('favourites.html')

@views.route('/get_quotes')
def get_quotes():
    url = "https://stoic-quotes.com/api/quotes"
    # get response data (stoic quote from above url)
    response = urllib.request.urlopen(url)
    data = response.read()
    # convert json data to python dict
    quotes = json.loads(data)

    return render_template('quotes_table.html', quotes = quotes)

