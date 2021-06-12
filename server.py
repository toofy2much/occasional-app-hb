from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import db, User, Contact, Occasion, Greeting, connect_to_db

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
    error = 'user already exists'
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
    error = 'user does not exist'

    user = crud.verify_user(email, password)

    if user:
        session['user_id'] = user.user_id
        flash('Next up Select contact')
        
        return redirect('/contacts')

    else:
        flash('Error email and password dont match')
    
        return render_template('homepage.html', error=error)

    #user = User.query.filter(User.email == email).first()
    #if user:
        #return redirect('/contacts')
    #else:
    #     new_user = User(fname= fname, lname = lname, email= email, password= password)
    #     db.session.add(new_user)
    #     db.session.commit(new_user)
    #     return redirect('/login')
    # return render_template('contact.html')



@app.route('/contacts', methods=['POST'])
def new_contact():
    """add contact info form""" 
    if 'user_id' in session:
        user_id = session['user_id']
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        error = 'contact already exists'
        # contact= request.form.get('contact')
        # crud.add_contact()
        # return render_template('contacts.html')
        if not crud.add_contact(fname, lname, email, phone, user_id):
            flash('A contact already exists with that email')
        else:
            flash('select your contact below to add special occasions')

        # Redirect to 
        return redirect('/contacts')
    else:
        flash('Login required')
        return redirect('/')


@app.route('/contacts') #endpoint returning table in html of saved contacts
def contact_table():
    """displays contact data from db in table format"""

    contact = Contact.query.all()

    return render_template('contacts.html', contact=contact)



@app.route('/select_contact', methods=['POST'])
def get_contact():
    """select contact into a form""" 
    
    contact= request.form.get('contact')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    error = 'contact does not exist'

    contact = crud.verify_contact(fname, lname)
    print(contact)
    if contact:
        session['contact_id'] = contact.contact_id
        flash('Next up Select contact')
        
        return redirect(f'/occasions/{contact.contact_id}')
    

    else:
        flash('Error contact doesnt match any entries')
    
        return render_template('contact.html', error=error)


@app.route('/occasions/<contact_id>')
def get_occasions(contact_id):
    if 'user_id' in session:
        user_id = session['user_id']
        contact = Contact.query.get(contact_id)
        occasions = contact.occasions
        greetings = []
        for occ in occasions:
            greeting = Greeting.query.filter_by(user_id=user_id, occasion_id=occ.occasion_id).first()
            greetings.append(greeting)
        print(greetings)
        return render_template('greetings.html', contact=contact, greetings=greetings)
    else:
        return redirect('/')


    
@app.route('/occasions/<contact_id>', methods=['POST'])
def add_occasion(contact_id):
    """select contact into a form""" 
    if 'user_id' in session:
        user_id = session['user_id']
        occasion = request.form.get('occasion')
        title = request.form.get('title')
        occasion_date = request.form.get('occasion_date')
        body = request.form.get("body")
        send_date = request.form.get("send_date")

        contact = Contact.query.get(contact_id)

        new_occasion = crud.add_occasion(contact.contact_id, title, occasion_date)
        new_greeting = crud.add_greeting(body, new_occasion.occasion_id, send_date, user_id)
        return redirect(f'/occasions/{contact.contact_id}')
    else:
        return redirect('/')
    # def add_greeting():
    #     if not greeting:
    #         session['occasion_id'] = ocasion.occasion_id
    #         session['greeting_id'] = greeting.greeting_id
    #         flash('hi')
            
    #         return redirect('/occasion')

    #     else:
    #         flash('Error can not compute')
        
    #         return render_template('greetings.html', error=error)


        #endpoint returning table in html of greetings
        # def greetings_table():
        #     """dispalys greetings sent from db in table format"""

        #     greeting = Greeting.query.all()

        #     return render_template('greetings.html', greeting=greeting)



    #if crud.verify_user(fname, lname):
    #     flash('Next up Select occasion')
    # else:
    #     flash('Error contact doesnt match any entries')

    # return redirect('/occasions')

 

    
    













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