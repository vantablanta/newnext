from email.policy import default
from . import db, login_manager
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  secure_password = db.Column(db.String, nullable=False)
  hoods = db.relationship('Hoods', backref='hoods', lazy=True)
  posts = db.relationship('Post', backref='author', lazy=True)
  hood = db.Column(db.String)

  @property
  def password(self):
    raise AttributeError('You cannot read the password attribute')

  @password.setter
  def password(self, password):
    self.secure_password = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.secure_password, password)

  def __repr__(self):
    return f"User('{self.username}')"


class Hoods(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  about = db.Column(db.String, nullable=False)
  # on button click update the memebers number
  members = db.Column(db.Integer, default=1)
  hood_pic = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # admin
  amenities = db.relationship('Amenities', backref='amenities', lazy=True)


class Amenities(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  police_contact = db.Column(db.String)
  hospital_contact = db.Column(db.String)
  hood_id = db.Column(db.Integer, db.ForeignKey('hoods.id'))


class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  content = db.Column(db.Text(), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
  date_posted = db.Column(db.DateTime, default=datetime.utcnow)

  # def save_post(self):
  #     db.session.add(self)
  #     db.session.commit()

  def __repr__(self):
    return f"Post('{self.title}', '{self.date_posted}')"


class Business(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  tel = db.Column(db.Integer)
  description = db.Column(db.Text(), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

  # def save_post(self):
  #     db.session.add(self)
  #     db.session.commit()

  def __repr__(self):
    return f"Business('{self.name}')"
