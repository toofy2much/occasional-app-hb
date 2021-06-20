from model import db, User, Contact, Occasion, Greeting, connect_to_db
from datetime import datetime

def add_user(fname, lname, email, phone, password):
    """checks user data with existing users"""  
    user = User.query.filter(User.email == email).first()

    if user:
        return False #'A user already exists with that email.'
    else:
        new_user = User(fname= fname, lname= lname, 
                        email= email, phone= phone, 
                        password= password)

        db.session.add(new_user)
        db.session.commit()

        return True        #redirect('/registration-form')


def verify_user(email, password):
    """takes user email to verify password"""
    
    user = User.query.filter(User.email == email).first()
    if user and password == user.password:
        return user
            
    else:
        return None

# def add_contact():
#     email = request.form['email']
#     phone = request.form['phone']

#     contact = Contact.query.filter(Contact.email == email).first()
#     if contact:
#         return 'A contact already exists with that email.'
#     else:
#         new_contact = Contact(fname=lname, lname=lname, email=email, 
#         phone= phone)
#         db.session.add(new_contact)
#         db.session.commit(new_contact)
#         return redirect('/contacts.html')

def add_contact(fname, lname, email, phone, user_id):
    """checks contact data with existing contacts"""  
    contact = Contact.query.filter(Contact.email == email).first()

    if contact:
        return False #'A contact already exists with that email.'
    else:
        new_contact = Contact(fname=fname, lname=lname, email=email, phone=phone, user_id=user_id)

        db.session.add(new_contact)
        db.session.commit()

        return True        


def verify_contact(fname, lname):
    """takes contacts first/name to verify contact"""
    
    contact = Contact.query.filter(Contact.fname == fname).first()
    if contact and lname == contact.lname:
        return contact
            
    else:
        return None
def add_occasion(contact_id, title, occasion_date):
    """occasion data"""
    occasion = Occasion(contact_id= contact_id, title= title, occasion_date= occasion_date)
    db.session.add(occasion)
    db.session.commit()

    return occasion

def add_greeting(body, occasion_id, send_date, user_id):
    """checks occasion data with existing contacts"""  
    greeting = Greeting(body=body, occasion_id=occasion_id, send_date=send_date, user_id=user_id)

    db.session.add(greeting)
    db.session.commit()

    return greeting       


def verify_greeting(greeting_id, send_date):
    """takes input from greeting_id and compares with send_date 
    to verify not a duplicate"""
    
    greeting = greeting.query.filter(greeting_id == greeting_id).first()
    if greeting and send_date == greeting.send_date:
        return greeting
            
    else:
        return none

def get_users_current_greetings(user_id):
    current_date= datetime.now()
    user_greetings= User.query.get(user_id).greetings

    return user_greetings



if __name__ == '__main__': 
    from server import app
    connect_to_db(app)
