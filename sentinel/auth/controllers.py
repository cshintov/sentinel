from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from sentinel import db

# Import module forms
from sentinel.auth.forms import LoginForm

# Import module models (i.e. User)
#from app.auth.models import User
from sentinel.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ the login in controller """
    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        user = User.objects().get(username=form.username.data)
        pass_hash = generate_password_hash(user.password)
        if user and check_password_hash(pass_hash, form.password.data):
            flash('Welcome %s' % user.username)
            #return render_template('auth/login.html', form=form)
            return redirect(url_for('home.welcome', username=user.username))
        flash('Wrong username or password', 'error')

    return render_template("auth/login.html", form=form)
