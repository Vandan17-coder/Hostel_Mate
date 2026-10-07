from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Optional

class ResourceForm(FlaskForm):
    title = StringField('Item Name / Book Title', validators=[DataRequired(), Length(max=200)], render_kw={'class': 'form-control', 'placeholder': 'e.g. Data Structures & Algorithms Textbook'})
    category = SelectField('Category', choices=[
        ('book', 'Books & Notes'),
        ('electronics', 'Electronics & Accessories'),
        ('sports', 'Sports Goods'),
        ('lab', 'Lab & Study Tools'),
        ('other', 'Other Utility')
    ], default='book', render_kw={'class': 'form-select'})
    description = TextAreaField('Description & Condition', validators=[DataRequired()], render_kw={'class': 'form-control', 'rows': 3, 'placeholder': 'Edition, condition, or terms for borrowing'})
    contact_info = StringField('Contact Info (Phone / Room # / WhatsApp)', validators=[DataRequired(), Length(max=100)], render_kw={'class': 'form-control', 'placeholder': 'Phone / WhatsApp / Hostel Room'})


class LostAndFoundForm(FlaskForm):
    item_type = SelectField('Report Type', choices=[
        ('lost', 'Lost Item'),
        ('found', 'Found Item')
    ], validators=[DataRequired()], render_kw={'class': 'form-select'})
    title = StringField('Item Name / Brief Title', validators=[DataRequired(), Length(max=200)], render_kw={'class': 'form-control', 'placeholder': 'e.g. Black Leather Wallet / Boat Earbuds'})
    category = StringField('Category', validators=[Optional(), Length(max=50)], default='Personal Belongings', render_kw={'class': 'form-control', 'placeholder': 'Electronics, ID Card, Clothing, Keys'})
    location = StringField('Location Lost / Found', validators=[DataRequired(), Length(max=150)], render_kw={'class': 'form-control', 'placeholder': 'e.g. Mess Hall Table 4 or Library 2nd Floor'})
    date_event = DateField('Date of Event', validators=[DataRequired()], render_kw={'class': 'form-control', 'type': 'date'})
    contact_info = StringField('Contact Phone / WhatsApp', validators=[DataRequired(), Length(max=100)], render_kw={'class': 'form-control', 'placeholder': 'Phone / WhatsApp number'})
    description = TextAreaField('Description & Identification Marks', validators=[DataRequired()], render_kw={'class': 'form-control', 'rows': 3, 'placeholder': 'Distinctive marks, color, brand, or details'})
