
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
