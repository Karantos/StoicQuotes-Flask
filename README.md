# Stoic Quotes Web App
An web app that shows random Stoic quotes to the user. Users can register and then save their favourite quotes to favourites.

App made as a final project for [Harvard CS50x course](https://cs50.harvard.edu/x/2023/).

Used **Flask** with **Jinja templating engine** for building the webpage. Used **SQLite** with **SQLAlchemy** to save users and their favourite quotes to db.

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

Below is more detailed description of what each file does.

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


### website/views.py
