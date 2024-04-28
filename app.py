from flask import Flask, session, redirect, render_template, url_for, abort
from models import db, connect_db, User
from forms import AddUser, LoginUser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SECRET_KEY'] = 'users'

connect_db(app)

with app.app_context():
    db.create_all()
    
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User, 'AddUser': AddUser}

#   ==============================================================
#       HOME PAGE
#   ==============================================================

@app.route('/')
def homepage():
    return redirect('/register')

#   ==============================================================
#       REGISTRATION
#   ==============================================================

@app.route('/register')
def show_user_form():
    form = AddUser()
    return render_template('register.html', form=form)

@app.route('/register', methods=['POST'])
def create_user():
    form = AddUser()
    
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first = form.first_name.data
        last = form.last_name.data
        
        user = User.register(
            name=name, pwd=pwd, email=email,
            first=first, last=last
        )
        session["user_id"] = user.username
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('show_user', username=session["user_id"]))
    else:
        return render_template('register.html', form=form)
    
#   ==============================================================
#       LOG IN / lOG OUT
#   ==============================================================

@app.route('/login')
def show_login_form():
    form = LoginUser()
    return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def log_in_user():
    form = LoginUser()
    
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        
        user = User.authenticate(name, pwd)
        
        if user:
            session["user_id"] = user.username
            return redirect(url_for('show_user', username=session["user_id"]))
        else:
            render_template('login.html', form=form)
    
@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return redirect('/')
            
#   ==============================================================
#       SECRET
#   ==============================================================

@app.route('/users/<string:username>')
def show_user(username):
    if "user_id" in session and username == session["user_id"]:
        user = User.query.filter_by(username=username).first()
        return render_template('user.html', user=user)
    else:
        abort(403)

#   --------------------------------------------------------------
#   PART FOUR
#   --------------------------------------------------------------

# @app.route('/secret')
# def secret_route():
#     if "user_id" in session:
#         return "You made it!"
#     else:
#         return redirect('/')

#   --------------------------------------------------------------
