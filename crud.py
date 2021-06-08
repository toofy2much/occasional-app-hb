from model import db, User, Contact, Occasion, Greeting, connect_to_db


def add_user(fname, lname, email, phone, password):
    
    user = User.query.filter(User.email == email).first()

    if user:
        return False #'A user already exists with that email.'
    else:
        new_user = User(fname= fname, lname= lname, 
        email= email, phone= phone, password= password)

        db.session.add(new_user)
        db.session.commit()

    return True        #redirect('/registration-form')


# takes user email to verify password

def verify_user(email, password):
    
    user = User.query.filter(User.email == email).first()
    if user:
        return password == user.password
            
    else:
        return False

def add_contact():
    email = request.form['email']
    phone = request.form['phone']

    contact = Contact.query.filter(Contact.email == email).first()
    if contact:
        return 'A contact already exists with that email.'
    else:
        new_contact = Contact(fname=lname, lname=lname, email=email, 
        phone= phone)
        db.session.add(new_contact)
        db.session.commit(new_contact)
        return redirect('/contacts.html')


if __name__ == '__main__': 
    from server import app
    connect_to_db(app)
