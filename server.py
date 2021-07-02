import os, sys, requests 


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
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
import urllib

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
os.system('source secrets.sh')

app.secret_key =  os.environ['SECRET']
app.jinja_env.undefined = StrictUndefined

#set the environment variables 
#send and sms

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
#giphy_api_key = os.environ['GIPHY_API_KEY']

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
                        # Replace the following with the API key generated.
            API_KEY = "SzpABjzHdXTtZ5pAhQ5ZHS93xVK6sN0g"
            endpoint = "https://api.giphy.com/v1/gifs/search"

            search_term = greeting.occasion.title
            print(search_term, "*********")
            params = {"api_key": API_KEY, "limit": 1, "q": search_term, "rating": "g"}
            response = requests.get(endpoint, params=params).json()

            #""_data = json.loads(f.read())
            # gif = response["data"][0]
            # title = gif["title"]
            if len(response["data"]) > 0:
                url = response["data"][0]["images"]["fixed_height"]["url"] #["url"]
                print(f"\n| url = {url}")
                print("*"*10, "\n dir response = ")
                print(dir(response))
                print("*"*10)
            else:
                url = "https://media.giphy.com/media/MuLGuy9Bx6skU/giphy.gif"
            print(contact.email)

            #with app.open_resource(response) as f:
                #msg.attach(response)response
            msg = Message(recipients= [contact.email],
                          html= "hello " + contact.fname + " " + greeting.body + " "+ "<img src='"+ url+"'/>",
                          subject= subject)
            print("************")
            print(msg)
            conn.send(msg)

            phone = greeting.occasion.contact.phone
            print(greeting.occasion.contact.phone)
            name = (greeting.occasion.contact.fname +" ")
            msg = client.messages.create(to="+1"+ phone, from_="+12156085643",   
                                        body = "hello " + name + greeting.body + " " + url) 
                                        #media_url= [url])
            print(phone)                        
            print(msg)                         

            phone = greeting.user.phone
            name = (greeting.user.fname + " ")
            sent_greeting = ("Occasion reminder was sent to " + greeting.occasion.contact.fname)
            client.messages.create(to="+1"+ phone, from_="+12156085643",
                                        body = "hello, " + name + sent_greeting)
            
            #print(client.message.sid) 
    
   
        return 'msg has been sent'  
#return redirect(/login)


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

    if crud.add_user(fname.title(), lname.title(), email, phone, password) :
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
        if not crud.add_contact(fname.title(), lname.title(), email, phone, user_id):
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
    contacts = Contact.query.order_by(Contact.fname.asc()).all()
    
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

       
print("*********stopping")


@app.route('/bulk', methods = ['GET'])
def send_greetings():
    """calls send_all funct to execute current greetings"""
    send_all()

    return 'all messages sent'
            

@app.route('/logout', methods=['POST'])
def logout():
    """return to homepage"""
    send_all()
    """sends currents greetings"""
    return redirect('/')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
           

   
