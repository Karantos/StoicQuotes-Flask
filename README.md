# Stoic Quotes Web App
An web app that shows random Stoic quotes to the user. Users can register and then save their favourite quotes to favourites.

App made as a final project for [Harvard CS50x course](https://cs50.harvard.edu/x/2023/).

Used **Flask** with **Jinja templating engine** for building the webpage. Used **SQLite** with **SQLAlchemy** to save users and their favourite quotes to db and **Flask-Login** to handle user auhthenthication.

### Video Demo: [Stoic Quotes Web App](https://studio.youtube.com/video/HtdNKQfF-dQ/edit)
[Here](https://studio.youtube.com/video/HtdNKQfF-dQ/edit) you can see a preview of Stoic Quotes Web App.

## Description
The structure of my project is:
* website
	* static
		* scripts.js
		* styles.css
	* templates
		* change_password.html
		* edit_profile.html
		* favourites.html
		* index.html
		* layout.html
		* login.html
		* quotes_table.html
		* register.html
	* \_\_init.py__
	* auth.py
	* models.py
	* views.py
* app.py

Below is more detailed description of what each file does:

### app.py
Script inside this file runs the application using a development server.

### website/\_\_init.py__
The code `db = SQLAlchemy()` creates a new instance of the SQLAlchemy class. This class is used to interact with a database. In this case, the database is a SQLite database named quotes.db. The database is created in the same folder as the Flask app. The SQLAlchemy class provides a number of methods for interacting with the database, such as `create_all()`, which creates all of the tables in the database, and `query()`, which allows you to select data from the database.

```
app = Flask(__name__)
app.config['SECRET_KEY'] = 'janrepar jflsjglalg'

# configures db location (sets location to flask app website folder)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///' + os.path.join(basedir, 'quotes.db')
db.init_app(app)
```
These lines inside `def create_app()` function create a new Flask app and configure it with a secret key. The secret key is used to encrypt cookies and other sensitive data. The SQLALCHEMY_DATABASE_URI configuration setting is set to the location of the database file. The `db.init_app(app)` line tells the SQLAlchemy instance to bind itself to the Flask app. This means that the SQLAlchemy instance will be available to all of the views and other components of the Flask app.

```
from .views import views
from .auth import auth

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
```
These lines register blueprints with the Flask app. Blueprints are a way to organize the code for a Flask app. The views blueprint contains the code for the views and the auth blueprint contains the code for the authentication of the user.

```
from .models import User, Quote

with app.app_context():
        db.create_all()
```
This line imports the User and Quote models from the models.py. The `with app.app_context()` line tells Flask to create a new application context. This context is used to access the SQLAlchemy instance and the database. The `db.create_all()` line creates all of the tables in the database.

```
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
```
This code initializes the Flask-Login extension. Flask-Login is a library that provides support for user authentication. The `login_manager.login_view = 'auth.login` setting is set to the URL of the login page. The `login_manager.init_app(app)` line tells Flask-Login to initialize itself with the Flask app.

```
@login_manager.user_loader
def load_user(id):
        return User.query.get(int(id))
```
This function is used to load a user from the database by their ID. The `login_manager.user_loader` decorator tells Flask-Login to use this function to load users.

### website/models.py
The code inside models.py defines two classes: `User` and `Quote`. These classes are used to represent users and quotes in a relational database.

The `User` class inherits from the `db.Model` class and the `UserMixin` class. The `db.Model` class is a base class for all SQLAlchemy models. The `UserMixin` class provides some useful methods for user authentication, such as `is_authenticated()` and `get_id()`.

In the `User` class `db.relationship()` method is used to define a relationship between two models. In this case, the `quotes` relationship defines a one-to-many relationship between the `User` model and the `Quote` model. This means that a user can have many quotes and a quote can only have one user.

### website/auth.py
Code inside auth.py handles user registration, login, logout, edit profile and change password and contains the corresponding routes.

The `/login` route is defined as follows:

```
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Username does not exist.', category='error')
    return render_template('login.html')
```
This route first checks if the request method is POST. If it is, the code gets the username and password from the request form. The code then queries the database for a user with the given username. If a user is found, the code checks the password against the user's password hash. If the password is correct, the code logs the user in and redirects to the index page. Otherwise, the code displays an error message.

The `/logout` route is defined as follows:

```
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
```
This route is only accessible to logged-in users. When a user logs out, the code clears the user's session and redirects to the login page.

The `/register` route is defined as follows:

```
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirm-password')

        user = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user:
            flash('Username taken', category='error')
        elif user_email:
            flash('Email already used', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters long.', category='error')
        elif password != confirmation:
            flash('Passwords do not match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters long.', category='error')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', category='success')
            return redirect(url_for('views.index'))
        return render_template('register.html')
    else:
        return render_template('register.html')
```
This route first checks if the request method is POST. If it is, the code gets the email, username, password, and confirmation password from the request form. The code then checks if a user with the given username or email already exists. If so, the code displays an error message.

The code then checks if the password and confirmation password match. If they do not match, the code displays an error message. If all of the checks pass, the code creates a new user with the given information and saves it to the database. The code then redirects the user to the index page.

The `/edit_profile` route is defined as follows:

```
@auth.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')

        user_id = User.get_id(current_user)

        if len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters long.', category='error')
        else:
            User.query.filter_by(id=user_id).update(dict(username=username, email=email))
            db.session.commit()
            flash('Profile updated!', category='success')
            return redirect(url_for('views.index'))
        return render_template('edit_profile.html')
    else:
        return render_template('edit_profile.html')
```
This route is only accessible to logged-in users. When a user visits this route, the code gets the user's ID from the session. The code then gets the user's email and username from the database.

If the request method is POST, the code gets the new email and username from the request form. The code then checks if the new email and username are valid. If they are not, the code displays an error message. 

If the checks pass, the code updates the user's email and username in the database. The code then redirects the user to the index page.

The `/change_password` route is defined as follows:

```
@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('password')
        new_password = request.form.get('new-password')
        confirmation = request.form.get('confirm-password')

        user_id = User.get_id(current_user)
        user = User.query.filter_by(id=user_id).first()

        if not check_password_hash(user.password, old_password):
            flash('Passwords is incorrect!', category='error')
        elif new_password != confirmation:
            flash('Passwords do not match.', category='error')
        elif len(new_password) < 7:
            flash('Password must be at least 7 characters long.', category='error')
        else:
            User.query.filter_by(id=user_id).update(dict(password=generate_password_hash(new_password, method='sha256')))
            db.session.commit()
            flash('Password changed!', category='success')
            logout_user()
            return redirect(url_for('auth.login'))
        return render_template('change_password.html')
    else:
        return render_template('change_password.html')
```
The route first checks if the request method is POST. If it is, the code gets the old password, new password, and confirmation password from the request form.

The code then gets the user ID of the currently logged-in user. The code then queries the database for the user with the given ID.

The code then checks if the old password entered by the user matches the password stored in the database. If it does not, the code displays an error message.

The code then checks if the new password and confirmation password match. If they do not match, the code displays an error message. If all of the checks pass, the code updates the user's password in the database. The code then logs the user out and redirects the user to the login page.

### website/views.py
The `/` route is defined as follows:

```
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
```
This route is the homepage of the application. It gets a stoic quotes from the https://stoic-quotes.com/api/quote URL and displays it on the page.

If the request method is POST, the code gets the text and author of the quote from the request form. The code then creates a new quote object and saves it to the database and the user can then view it on `/favourites` page. The code then redirects the user to the homepage.

The `/favourites` route is defined as follows:

```
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
        user_id = User.get_id(current_user)
        quotes = Quote.query.filter_by(user_id=user_id).all()

        if quotes:
            return render_template('favourites.html', quotes = quotes)

        else:
            flash('You have no quotes added to favourites.', category='error')                 
            return redirect(url_for('views.index'))
```
This route is used to manage the favorites of the logged-in user. If the request method is POST, the code gets the ID of the quote to be deleted from the request form. The code then deletes the quote from the database and redirects the user to the favorites page.

If the request method is GET, the code gets the ID of the logged-in user. The code then gets all of the quotes that the user has added to their favorites and renders the favorites page with the list of quotes.

The `/get_quotes` route is defined as follows:

```
@views.route('/get_quotes')
def get_quotes():
    url = "https://stoic-quotes.com/api/quotes"
    # get response data (stoic quote from above url)
    response = urllib.request.urlopen(url)
    data = response.read()
    # convert json data to python dict
    quotes = json.loads(data)

    return render_template('quotes_table.html', quotes = quotes)
```
This route is used to get a list of stoic quotes from the https://stoic-quotes.com/api/quotes URL. The code then converts the JSON data to a Python dictionary and renders the quotes table page with the list of quotes.

### static/scripts.js
THis file contains JavaScript that uses AJAX to update only part of a web page. AJAX stands for Asynchronous JavaScript and XML. It is a technique that allows web pages to communicate with a server without having to reload the entire page.

The code is divided into three parts:

The first part binds the click event to the element with id `#get-quotes`. When the user clicks on this element, the code calls the `load()` method on the element with id `#quotes-table`. The `load()` method tells the browser to load the content of the `/get_quotes` route (that renders `quotes-table.html`) into the element with id `#quotes-table`.

The second part binds the click event to the element with id `#get-quote`. When the user clicks on this element, the code calls the `load()` method on the element with id `#quote`. The `load()` method tells the browser to load the content of the `/ #quote` route (part of content in `index.html` with id of `#quote`) into the element with id `#quote`. 

The third part binds the keypress event to the element with id `#navbarNavDarkDropdown`. When the user presses a key on this element, the code calls the `dropdown('toggle')` method on the element and tells the browser to toggle the dropdown menu.

### static/styles.css
In this file is come css code that adds some custom styling to elements `.table` class.

### templates/..
In templates folder there are multiple html files that show various parts of the page, i.e. `index.html`, `layout.html`, `register.html`, `login.html`. **Jinja templating engine** was used for dynamic content.

## Tools used
* Flask
* Jinja2
* Werkzeug
* Flask-Login
* Flask-SQLAlchemy

