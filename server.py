from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
#app.secret_key = "secret"
app.jinja_env.undefined = StrictUndefined

# @app.errorhandler(404)
# def not_found(e): 
#     return render_template("404.html")


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


@app.route('/register', methods=['POST'])
def new_user():
    user= request.form.get('fname','lname','email','phone','password')
    crud.add_user('user')
    return render_template('homepage.html')


    @app.route('/login', methods=['POST'])
    def current_user():
        request.form.get['user']
        crud.verify_user()
        return render_template('homepage.html')

# @app.route('/handle-login', methods=['POST'])
# def handle_login():
#     """Log user into application."""

#     user= request.form['email']
#     password = request.form['password']

#     if email == 'password':   
#         session['user'] = fname
#         alert(f'Logged in as {fname}')
#         return redirect('/   ')

#     else:
#       
#         return redirect('/login')




# Replace this with routes and view functions!


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)