import os, sys 


print(os.environ)

from flask import (Flask, render_template, request, escape, flash, session,
                   url_for,redirect, jsonify, abort)
from flask_mail import Mail, Message 
from model import db, User, Contact, Occasion, Greeting, connect_to_db
from datetime import datetime
from twilio.rest import Client #, logging
#from twilio.twiml.messaging_response import Message #, MessagingResponse
#from twilio.base.exceptions import TwilioRestException
from reminder_json_helper import read_reminder_json, create_reminder_json, write_reminder_json
import uuid

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
os.system('source secret.sh')

app.secret_key =  os.environ['SECRET']
app.jinja_env.undefined = StrictUndefined

#set the environment variables 
#send and sms

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)



app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBUG'] =  True  
app.config['MAIL_USERNAME'] = 'occasionreminder215@gmail.com'
app.config['MAIL_PASSWORD'] = 'DingDong'
app.config['MAIL_DEFAULT_SENDER'] = 'occasionreminder215@gmail.com'
app.config['MAIL_MAX_EMAILS'] = 5
#app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False 

mail = Mail(app)


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

    contacts = Contact.query.all()

    return render_template('contacts.html', contacts=contacts)



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
    
        return redirect("/contacts")

@app.route('/occasions/<contact_id>')
def get_occasions(contact_id):
    if 'user_id' in session:
        user_id = session['user_id']
        contact = Contact.query.get(contact_id)
        occasions = contact.occasions
        greetings = []
        for occ in occasions:
            greeting = Greeting.query.filter_by(user_id=user_id, occasion_id=occ.occasion_id).first()
            if greeting:
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


# @app.route('/send')
# def test_mail():
#     msg = Message('hi test email', recipients=['occasionreminder215@gmail.com'])
#     #msg.add_recipient('')
#     msg.body= 'test email'
#     # contact.greeting.body
#     mail.send(msg)
    

#     return 'msg has been sent'

@app.route('/bulk')    
def send_all():   #opening connection with built in method
    """sends users current greetings emails and texts"""

    print('*******in send_all_route*****')
    
    user_id = session.get('user_id')
    greetings = crud.get_users_current_greetings(user_id)
    crud.mark_sent_greetings(greetings)
    
    #crud function take all user greeting data and compare send_date to current date 
   
    with mail.connect() as conn:
        for greeting in greetings:
    
           
            occ = greeting.occasion
            contact = occ.contact
            subject = "hello, " + contact.fname
            print(contact.email)
            msg = Message(recipients= [contact.email],
                          body= greeting.body,
                          subject= subject)
            print("************")
            print(msg)
            conn.send(msg)

            phone = greeting.occasion.contact.phone
            name = (greeting.occasion.contact.fname +" ")
            client.messages.create(to="+1"+ phone, from_="+12156085643",
                                        body = "hello, " + name + greeting.body)

            phone = greeting.user.phone
            name = (greeting.user.fname + " ")
            sent_greeting = ("Occasion reminder was sent to " + greeting.occasion.contact.fname)
            client.messages.create(to="+1"+ phone, from_="+12156085643",
                                        body = "hello, " + name + sent_greeting)

    return 'msg has been sent'

 
   

    

print("*********stopping")
            #occ = greeting.occasion
            #contact = occ.contact
            # to = "+1" + contact.phone
           

    #User.query.get(session['user_id']).filter(Greeting.send_date== x).all()
                #(user_id=session.get('user_id'))
    #.get(session['user_id'])
    #crud.get_users_current_greetings()
    
    #contact_phone=["+1" (contact.phone)]
    #for greeting in greetings:  
        #phone = greeting.occasion.contact.phone
        #name = (greeting.occasion.contact.fname +" ")
        #message = client.messages.create(to="+1"+ phone, from_="+12156085643",
                                        #body = "hello, " + name + greeting.body)

            
    #print(message.sid) 

    #return 'msg has been sent' # adjust this message to reflect state

# use a second function or this reminder api

# @app.route('/api/reminders', methods=['GET'])
# def get_reminders():
#  """getting all reminders"""

#     reminders = read_reminder_json()
#     return jsonify({'reminders': reminders})

# @app.route('/api/reminders', methods=['POST'])
# def create_reminder():
#     """create reminders"""
#     req_data = request.get_json()

#     if not all(item in req_data for item in ("phone_number", "message", "due_date")):
#         abort(400)

#     reminder = {
#         'id': uuid.uuid4().hex,
#         'phone_number': req_data['phone_number'],
#         'message': req_data['message'],
#         'interval': 'monthly',
#         'due_date': req_data['due_date']
#     }


#     create_reminder_json(reminder)
#     return jsonify({'reminder': reminder}), 201


# @app.errorhandler(400)
# def bad_request(error):
#     return jsonify({'error': 'Bad Request'}), 400

# @app.route('/api/reminders/<reminder_id>', methods=['DELETE'])
# def delete_reminder(reminder_id):
#     reminders = read_reminder_json()
#     reminder = [reminder for reminder in reminders if reminder['id'] == reminder_id]
#     if len(reminder) == 0:
#         abort(404)
#     reminders.remove(reminder[0])
#     data = {}
#     data['reminders'] = reminders
#     write_reminder_json(data)
#     return jsonify({'message': 'Reminder has been removed successfully'})


# @app.errorhandler(404)
# def not_found(error):
#     """delete reminder"""
#     return jsonify({'error': 'Not Found'}), 404


# add a button to send todays messages if we cant cronjob
# would be cool if just sent on the date without logging 
# or hitting a button if it was hosted 

@app.route('/logout', methods=['POST'])
def logout():
    """return to homepage"""
   
    return redirect('/')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)