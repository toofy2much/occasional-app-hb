import os
import json
from random import choice, randint
from datetime import datetime

import crud
from model import *
import server

os.system('dropdb reminder')
os.system('createdb reminder')


#connect to the database and call db.create_all:

connect_to_db(server.app)
db.create_all()


test_user = User(fname='test_first',lname='test_last', email='test@test.test', 
                     phone= "6666666666", password='test')
db.session.add(test_user) 
db.session.commit()


test_contact= Contact(fname='cnt_first',lname='cnt_last', email='cntt@test.test', 
                     phone= "9999999999")
db.session.add(test_contact) 
db.session.commit()

test_occasion = Occasion(title='test_title', occasion_date='12/12/2021')  
db.session.add(test_occasion) 
db.session.commit()


test_greeting= Greeting(body='this is a test',send_date='11/13/2021')
db.session.add(test_greeting) 
db.session.commit()

#with open('data/"".json') as f:
    #""_data = json.loads(f.read())

