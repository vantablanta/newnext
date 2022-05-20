from . import auth_blueprint
from flask import render_template,url_for,flash,redirect,request
from .forms import SignupForm,LoginForm
from flask_login import login_user,login_required,logout_user
from .. import db
from ..models import Users, Hoods


@auth_blueprint.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user is not None:
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('main_blueprint.home'))
        flash('Invalid username or Password. SIgn up or try again.')
    return render_template('auth/login.html', form=form)



@auth_blueprint.route('/signup', methods = ["GET","POST"])
def signup():
    form = SignupForm()
    hoods = Hoods.query.all()
    if form.validate_on_submit():
        user = Users(email = form.email.data, username = form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth_blueprint.login'))
    return render_template('auth/signup.html', form = form, hoods = hoods)



@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_blueprint.home"))




