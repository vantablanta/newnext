from . import main_blueprint
from flask import flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from .forms import AddHoodForm, BusinessForm, PostForm
from ..models import Business, Hoods, Post, Users
from .. import db, photos
from werkzeug.utils import secure_filename
import uuid
import os


@main_blueprint.route('/')
def home():
    hoods = Hoods.query.all()
    return render_template('index.html',hoods=hoods)


@main_blueprint.route('/add_hood', methods=['POST', 'GET'])
def addhood():
    form = AddHoodForm()
    if form.validate_on_submit():
        user_id = current_user._get_current_object().id
        file_name = form.hood_pic.data
        pic_file_name = secure_filename(file_name.filename)
        unique_pic_name = str(uuid.uuid1()) + '_' + pic_file_name
        hood_pic = unique_pic_name
        hood = Hoods(name=form.name.data, about=form.about.data,hood_pic=hood_pic, user_id=user_id)

        db.session.add(hood)
        db.session.commit()

        filename = photos.save(form.hood_pic.data)
        path = f'{filename}'
        hood.hood_pic = path
        return redirect(url_for('main_blueprint.all_hoods'))
    return render_template('add_hood.html', form=form)


@main_blueprint.route('/all_hoods')
def all_hoods():
    hoods = Hoods.query.all()
    return render_template('all_hoods.html',hoods=hoods)


@main_blueprint.route('/post', methods=['POST', 'GET'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        user_id = current_user._get_current_object().id
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main_blueprint.hoodpage', hood_id=id))
    return render_template('post.html', form=form)


@main_blueprint.route('/business', methods=['POST', 'GET'])
def new_business():
    form = BusinessForm()
    if form.validate_on_submit():
        user_id = current_user._get_current_object().id
        business = Business(name=form.name.data, email=form.email.data,
                            tel=form.tel.data, description=form.description.data)
        db.session.add(business)
        db.session.commit()

        return redirect(url_for('main_blueprint.hoodpage', hood_id=id))
    return render_template('business.html', form=form)


@main_blueprint.route('/hoodpage/<int:hood_id>')
def hoodpage(hood_id):
    posts = Post.query.all()
    businesses = Business.query.all()
    hood = Hoods.query.get(hood_id)
    return render_template('hoodpage.html', posts=posts, businesses=businesses, hood=hood)

    




@main_blueprint.route('/dashboard', methods = ['GET','POST'])
@login_required
def dashboard():
    return render_template('/profile/dashboard.html')