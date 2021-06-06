
 #@app.route('/register', methods=['POST'])
# def add_user():
#     email = request.form['email']
#     password = request.form['password']

#     user = User.query.filter(User.email == email).first()
#     if user:
#         return 'A user already exists with that email.'
#     else:
#         new_user = User(fname=lname, lname=lname, email=email, 
#         phone= phone password=password)
#         db.session.add(new_user)
#         db.session.commit(new_user)

#         return redirect('/registration-form')

#@app.route('/login', methods=['POST'])
# def verify_user():
#     email = request.form['email']
#     password = request.form['password']

#     user = User.query.filter(User.email == email).first()
#     if user:
#         return 'A user already exists with that email.'
#     else:
#         new_user = User(fname= fname, lname = lname, email= email, password= password)
#         db.session.add(new_user)
#         db.session.commit(new_user)
             return redirect('/login-form')

