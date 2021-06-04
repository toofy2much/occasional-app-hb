import model.py


#test_user = User(fname='test_first',lname='test_last', email='test@test.test', 
#                      phone= '6666666666', password='test')
#     db.session.add(test_user) 
#     db.session.commit()


# test_contact= Contact(fname='cnt_first',lname='cnt_last', email='cntt@test.test', 
#                      phone= '9999999999', date='10/10/2021')
#     db.session.add(test_contact) 
#     db.session.commit()

# test_occasion = Occasion(title='test_title', date='12/12/2021',  
#                      reminder_date= '12/13/2012')
#     db.session.add(test_occasion) 
#     db.session.commit()


# test_greeting= Greeting(body='this is a test',date='11/13/2021')
#     db.session.add(test_gretting) 
#     db.session.commit()



# @app.route('/register', methods=['POST'])
# def register_user():
#     email = request.form['email']
#     password = request.form['password']

#     user = User.query.filter(User.email == email).first()
#     if user:
#         return 'A user already exists with that email.'
#     else:
#         new_user = User(email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit(new_user)

#         return redirect('/login-form')
