from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, EqualTo, Length, Email 

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class SignupForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('New Password', [DataRequired(),EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class VoluntierRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    mob = StringField('Mobile No', validators=[DataRequired(), Length(10)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    quallifaications = StringField('Quallifactions', validators=[DataRequired()])
    state = StringField('State', [DataRequired()])
    district = StringField('District', [DataRequired()])
    bio = TextAreaField('Bio', [DataRequired()])
    gov_doc = FileField('Upload Aadhar', [DataRequired(), FileRequired()])
    password = PasswordField('New Password', [DataRequired(),EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class MessgeForm(FlaskForm):
    voluntier = StringField('voluntier', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])