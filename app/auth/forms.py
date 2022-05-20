from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField,PasswordField,SubmitField,BooleanField, EmailField
from wtforms.validators import DataRequired,EqualTo
from ..models import Users

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me!')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    email = EmailField('Your Email Address', validators=[DataRequired()])
    username = StringField('Enter Your Username', validators=[DataRequired()])
    password = PasswordField('Password',validators = [DataRequired(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
        if Users.query.filter_by(email = data_field.data).first():
            raise ValidationError("The Email has already been taken!")
    
    def validate_username(self, data_field):
        if Users.query.filter_by(username = data_field.data).first():
            raise ValidationError("The username has already been taken")