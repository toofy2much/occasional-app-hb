import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

#connect to the database and call db.create_all:

# model.connect_to_db(server.app)
# model.db.create_all()
