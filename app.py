from flask import Flask, session, redirect, render_template, url_for, abort
from models import db, connect_db, User, Feedback
from forms import AddUser, LoginUser, AddFeedback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SECRET_KEY'] = 'users'

connect_db(app)

with app.app_context():
    db.create_all()
    
@app.shell_context_processor
def make_shell_context():
    if "user_id" in session:
        user = User.query.filter_by(username=session["user_id"]).first()
    else:
        user = None
    return {'app': app, 'db': db, 'User': User, 'AddUser': AddUser, 'user': user}

#   ==============================================================
#       HOME PAGE
#   ==============================================================

@app.route('/')
def homepage():
    if "user_id" in session:
        return redirect(url_for('show_user', username=session["user_id"]))
    else:
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
            form.password.errors = ["Invalid username or password"]
    
    return render_template('login.html', form=form)
    
@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return redirect('/')
            
#   ==============================================================
#       HANDLE USER DATA
#   ==============================================================

@app.route('/users/<string:username>')
def show_user(username):
    if "user_id" in session and username == session["user_id"]:
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('user.html', user=user)
        else:
            abort(403)
    else:
        abort(403)
        
@app.route('/users/<string:username>/delete')
def delete_user(username):
    if "user_id" in session and session["user_id"] == username:
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
        session.pop("user_id", None)
        return redirect('/')
    
#   ==============================================================
#       HANDLE FEEDBACK
#   ==============================================================

@app.route('/users/<string:username>/feedback/add')
def show_feedback_form(username):
    if "user_id" in session and session["user_id"] == username:
        user = User.query.filter_by(username=username).first()
        form = AddFeedback()
        return render_template('add_feedback.html', form=form, user=user)
    else:
        return redirect('/')
    
@app.route('/users/<string:username>/feedback/add', methods=['POST'])
def create_feedback(username):
    if "user_id" in session and session["user_id"] == username:
        form = AddFeedback()
        
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            f_user = session["user_id"]
            
        fb = Feedback(title=title, content=content, username=f_user)
        db.session.add(fb)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return redirect('/')
    
@app.route('/feedback/<int:f_id>/update')
def show_update_feedback_form(f_id):
    fb = Feedback.query.filter_by(id=f_id).first()
    if fb:
        form = AddFeedback(obj=fb)
        return render_template('update_feedback.html', form=form, fb=fb)
    else:
        abort(403)

@app.route('/feeback/<int:f_id>/update', methods=['POST'])
def update_feedback(f_id):
    fb = Feedback.query.filter_by(id=f_id).first()
    form = AddFeedback(obj=fb)
    if form.validate_on_submit():
        if "user_id" in session and fb.user.username == session["user_id"]:
            fb.title = form.title.data
            fb.content = form.content.data
            fb.username = session["user_id"]
            
            db.session.add(fb)
            db.session.commit()
            return redirect(f'/users/{session["user_id"]}')
        else:
            abort(403)
    
    else:
        return render_template('update_feedback.html', form=form)
    
@app.route('/feedback/<int:f_id>/delete')
def delete_feedback(f_id):
    fb = Feedback.query.filter_by(id=f_id).first()
    if fb.username == session["user_id"]:
        db.session.delete(fb)
        db.session.commit()
        return redirect(f'/users/{session["user_id"]}')
    else:
        return redirect(f'/feedback/{fb.id}/update')

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
