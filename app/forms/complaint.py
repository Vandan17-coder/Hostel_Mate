from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

class ComplaintForm(FlaskForm):
    title = StringField('Complaint Title', validators=[DataRequired(), Length(max=200)], render_kw={'class': 'form-control', 'placeholder': 'Brief title of problem'})
    category = SelectField('Category', choices=[
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('cleanliness', 'Cleanliness & Hygiene'),
        ('wifi', 'Wi-Fi & Internet'),
        ('furniture', 'Furniture & Carpentry'),
        ('other', 'Other')
    ], validators=[DataRequired()], render_kw={'class': 'form-select'})
    priority = SelectField('Priority Level', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium', render_kw={'class': 'form-select'})
    room_number = StringField('Room Number', validators=[DataRequired(), Length(max=20)], render_kw={'class': 'form-control', 'placeholder': 'e.g. 302'})
    hostel_block = StringField('Hostel Block', validators=[DataRequired(), Length(max=50)], default='Block A', render_kw={'class': 'form-control', 'placeholder': 'e.g. Block A'})
    description = TextAreaField('Detailed Description of Issue', validators=[DataRequired()], render_kw={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed explanation of the complaint...'})


class ComplaintStatusForm(FlaskForm):
    status = SelectField('Select Status', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected')
    ], validators=[DataRequired()], render_kw={'class': 'form-select'})
    admin_remarks = TextAreaField('Official Resolution Remarks / Action Plan', validators=[Optional()], render_kw={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. Electrician assigned, work scheduled for tomorrow 10 AM.'})
