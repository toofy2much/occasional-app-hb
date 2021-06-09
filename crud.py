from model import db, User, Contact, Occasion, Greeting, connect_to_db


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
    if user:
        return password == user.password
            
    else:
        return False

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

def add_contact(fname, lname, email, phone):
    """checks contact data with existing contacts"""  
    contact = Contact.query.filter(Contact.email == email).first()

    if contact:
        return False #'A contact already exists with that email.'
    else:
        new_contact = Contact(fname= fname, lname= lname, 
                              email= email, phone= phone)

        db.session.add(new_contact)
        db.session.commit()

    return True        


def verify_contact(fname, lname):
    """takes contacts first/name to verify password"""
    
    contact = Contact.query.filter(Contact.fname == fname).first()
    if contact:
        return lname == contact.lname
            
    else:
        return False




if __name__ == '__main__': 
    from server import app
    connect_to_db(app)
