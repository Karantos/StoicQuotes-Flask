from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import urllib.request, json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass

    else:
        url = "https://stoic-quotes.com/api/quotes?nume=10"
        # get response data (stoic quote from above url)
        response = urllib.request.urlopen(url)
        data = response.read()
        # convert json data to python dict
        dict = json.loads(data)

        quote = dict.pop()

        return render_template('index.html', results = dict, quote = quote)

@views.route('/favourites')
@login_required
def favourites():
    return render_template('favourites.html')
