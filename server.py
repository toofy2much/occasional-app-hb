from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import db, User, Contact, Occasion, Greeting, connect_to_db
from model import db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "secret"
app.jinja_env.undefined = StrictUndefined


# Access the request object
# Store session info
# Redirect to another route?
# Connect to your database
# Call CRUD functions

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route('/register', methods=['POST'])
def new_user():
    """collects data from a user in a form to 
    register a new user and add data to db"""
    
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    
    # Check if user with given email already exists

    #check_user = User.query.filter_by(email=email).first()

    if crud.add_user(fname, lname, email, phone, password):
        flash('Created a user! Now you can log in.')
    else:
        # If not, create new user and add to database
        
        # user = User(
        #     fname=fname,
        #     lname=lname,
        #     email=email,
        #     phone=phone,
        #     password=password
        # )
        # db.session.add(user)
        # db.session.commit()
        
        
        flash("You've already registered, please log in!")

    # Redirect to homepage
    return redirect('/')

@app.route('/login', methods=['POST'])
def get_login():
    """add login info to form""" 
    
    user= request.form.get('user')
    email = request.form.get('email')
    password = request.form.get('password')


    if crud.verify_user(email, password):
        flash('Next up Select contact')
    else:
        flash('Error email and password dont match')
    return redirect('/contacts')
    #user = User.query.filter(User.email == email).first()
    #if user:
        #return redirect('/contacts')
    #else:
    #     new_user = User(fname= fname, lname = lname, email= email, password= password)
    #     db.session.add(new_user)
    #     db.session.commit(new_user)
    #     return redirect('/login')
    # return render_template('contact.html')

@app.route('/contacts')
def contact_page():
    """View contact/occasion page"""

    return render_template('contacts.html')



@app.route('/contacts', methods=['POST'])
def new_contact():
    """add contact info form""" 

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # contact= request.form.get('contact')
    # crud.add_contact()
    # return render_template('contacts.html')
    if crud.add_contact(fname, lname, email, phone):
        flash('A contact already exists with that email')
    else:
        flash('select your contact below to add special occasions')

    # Redirect to 
    return redirect('/contacts')

@app.route('/select_contact', methods=['GET'])
def get_contact():
    """add login info to form""" 
    
    contact= request.form.get('contact')
    fname = request.form.get('fname')
    lname = request.form.get('lname')


    if crud.verify_user(fname, lname):
        flash('Next up Select occasion')
    else:
        flash('Error contact doesnt match any entries')

    return redirect('/occasions')















#should we be trying to "GET" by ID </>?
# @app.route('/contacts/<contact_id>', method= [GET])
# def show_contact():
#     """Displays contact info."""
#     contact = crud.get_contact(contact_id)
#     return render_template('contacts.html', contact=contact)



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







if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)