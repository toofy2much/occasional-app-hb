from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#app.secret_key = "SECRET"

class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    #should there a min and max digits for password and number*
    


    def __repr__(self):
        """Show info about users."""

        return f"""<User user_id={self.user_id} fname={self.fname}
                lname={self.lname} email={self.email} phone={self.phone}
                password={self.password}>"""
       
class Contact(db.Model):
    """Data model for a contacts."""
     
    __tablename__ = "contacts"
 
    contact_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref= "contacts")
    #should there a min and max digits for date?*


    def __repr__(self):
        """Show info about users."""

        return f"""<Contact contact_id={self.contact_id} fname={self.fname}
                lname={self.lname} email={self.email} phone={self.phone}>"""
       


class Occasion(db.Model):
    """Data model for a occasions."""
     
    __tablename__ = "occasions"


    occasion_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    title = db.Column(db.String, nullable=False)
    occasion_date = db.Column(db.DateTime, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    
    #should there a min and max digits for date?*

    contact = db.relationship("Contact", backref= "occasions")
   
    
    def __repr__(self):
        """Show info about occasions."""

        return f"""<Occasion occasion_id={self.occasion_id}
                 title={self.title} occasion_date={self.occasion_date}>"""
                 

class Greeting(db.Model):
    """Data model for a greetings."""
     
    __tablename__ = "greetings"
       
    greeting_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True)
    body = db.Column(db.Text, nullable=False)                         
    occasion_id = db.Column(db.Integer, db.ForeignKey("occasions.occasion_id"))
    send_date = db.Column(db.DateTime,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    sent = db.Column(db.Boolean, default= False)

                                                         

    occasion = db.relationship("Occasion", backref= "greetings")
    user = db.relationship("User", backref= "greetings")

    
    def __repr__(self):
        """Show info about greetings."""

        return f"""<Greeting greeting_id={self.greeting_id}
                body={self.body} 
                send_date={self.send_date}>"""


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///reminder"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to db!")
    #db.create_all()
    #test_user = User(fname='test_first',lname='test_last', email='test@test.test', 
    #                 phone= 6666666666, password='test')
    #db.session.add(test_user) 
    #db.session.commit()


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)

