from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "secret"
app.jinja_env.undefined = StrictUndefined


#You’ll need to import a couple more items before you’re able to

# Render templates

# Access the request object

# Flash messages

# Store session info

# Redirect to another route?

# Connect to your database

# Call CRUD functions


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')






# Replace this with routes and view functions!


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)