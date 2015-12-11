from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask.ext.login import login_user , logout_user , current_user , login_required

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

from sentinel import db, login_manager

# Import module forms
from sentinel.auth.forms import LoginForm

# Import module models
from sentinel.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ the login controller """
    if session.get('username'):
        username = session.get('username')
        nextpage = request.args.get('next')
        return redirect(nextpage or url_for('home.welcome', username=username))
    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        user = User.objects(username=form.username.data)[0]
        pass_hash = generate_password_hash(user.password)
        # authenticate the user and create the session
        if user and check_password_hash(pass_hash, form.password.data):
            login_user(user)
            session['username'] = user.username
            flash('Welcome %s' % user.username)
            nextpage = request.args.get('next')
            return redirect(nextpage or url_for('home.welcome', username=user.username))
        flash('Wrong username or password', 'error')

    return render_template("auth/login.html", form=form)

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    user = User.objects().get(username=username)
    return user

@auth.route("/logout")
@login_required
def logout():
    print logout_user()
    session.pop('username', None)
    return redirect(url_for('auth.login'))

