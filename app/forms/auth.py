from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class UserRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)], render_kw={'placeholder': 'Username', 'class': 'form-control'})
    first_name = StringField('First Name', validators=[Optional(), Length(max=150)], render_kw={'placeholder': 'First Name', 'class': 'form-control'})
    last_name = StringField('Last Name', validators=[Optional(), Length(max=150)], render_kw={'placeholder': 'Last Name', 'class': 'form-control'})
    email = EmailField('Email Address', validators=[Optional(), Email(), Length(max=254)], render_kw={'placeholder': 'Email Address', 'class': 'form-control'})
    
    role = SelectField('Account Role', choices=[('student', 'Student'), ('admin', 'Hostel Admin / Warden')], default='student', render_kw={'class': 'form-select'})
    roll_number = StringField('Roll Number', validators=[Optional(), Length(max=20)], render_kw={'placeholder': 'e.g. 2026CS101', 'class': 'form-control'})
    room_number = StringField('Room Number', validators=[Optional(), Length(max=20)], render_kw={'placeholder': 'e.g. 302', 'class': 'form-control'})
    hostel_block = StringField('Hostel Block', validators=[Optional(), Length(max=50)], default='Block A', render_kw={'placeholder': 'e.g. Block A', 'class': 'form-control'})
    phone = StringField('Phone Number', validators=[Optional(), Length(max=15)], render_kw={'placeholder': '+91 9876543210', 'class': 'form-control'})
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={'placeholder': 'Choose Password', 'class': 'form-control'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match!')], render_kw={'placeholder': 'Confirm Password', 'class': 'form-control'})


class LoginForm(FlaskForm):
    username = StringField('Username / Roll Number', validators=[DataRequired()], render_kw={'placeholder': 'Enter username (e.g. student1)', 'class': 'form-control'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Enter password', 'class': 'form-control'})


class ProfileUpdateForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional(), Length(max=150)], render_kw={'class': 'form-control'})
    last_name = StringField('Last Name', validators=[Optional(), Length(max=150)], render_kw={'class': 'form-control'})
    email = EmailField('Email Address', validators=[Optional(), Email()], render_kw={'class': 'form-control'})
    roll_number = StringField('Roll Number', validators=[Optional(), Length(max=20)], render_kw={'class': 'form-control'})
    room_number = StringField('Room Number', validators=[Optional(), Length(max=20)], render_kw={'class': 'form-control'})
    hostel_block = StringField('Hostel Block', validators=[Optional(), Length(max=50)], render_kw={'class': 'form-control'})
    phone = StringField('Phone Number', validators=[Optional(), Length(max=15)], render_kw={'class': 'form-control'})
    emergency_contact = StringField('Emergency Contact', validators=[Optional(), Length(max=15)], render_kw={'class': 'form-control'})
    bio = TextAreaField('Bio / Notes', validators=[Optional()], render_kw={'class': 'form-control', 'rows': 3})
