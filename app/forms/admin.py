from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class AdminStudentEditForm(FlaskForm):
    role = SelectField('Account Role', choices=[
        ('student', 'Student'),
        ('admin', 'Hostel Admin / Warden')
    ], validators=[DataRequired()], render_kw={'class': 'form-select'})
    roll_number = StringField('Roll Number', validators=[Optional(), Length(max=20)], render_kw={'class': 'form-control', 'placeholder': 'e.g. 2026CS101'})
    room_number = StringField('Assigned Room Number', validators=[DataRequired(), Length(max=20)], render_kw={'class': 'form-control', 'placeholder': 'e.g. 302-B'})
    hostel_block = StringField('Hostel Block', validators=[DataRequired(), Length(max=50)], default='Block A', render_kw={'class': 'form-control', 'placeholder': 'e.g. Block A'})
    phone = StringField('Phone Number', validators=[Optional(), Length(max=15)], render_kw={'class': 'form-control', 'placeholder': '+91 9876543210'})
