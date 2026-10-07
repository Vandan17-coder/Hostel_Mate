from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class MessMenuForm(FlaskForm):
    day = SelectField('Day of Week', choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], validators=[DataRequired()], render_kw={'class': 'form-select'})
    meal_type = SelectField('Meal Type', choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Evening Snacks'),
        ('dinner', 'Dinner')
    ], validators=[DataRequired()], render_kw={'class': 'form-select'})
    items = TextAreaField('Menu Items', validators=[DataRequired()], render_kw={'class': 'form-control', 'rows': 3, 'placeholder': 'Paneer Butter Masala, Roti, Rice, Dal'})
    timing = StringField('Timing', validators=[Optional(), Length(max=50)], render_kw={'class': 'form-control', 'placeholder': 'e.g., 7:30 AM - 9:30 AM'})


class MessReviewForm(FlaskForm):
    rating = IntegerField('Rating (1 to 5 Stars)', validators=[DataRequired(), NumberRange(min=1, max=5)], render_kw={'class': 'form-control', 'min': 1, 'max': 5})
    meal_type = SelectField('Meal Category', choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Evening Snacks'),
        ('dinner', 'Dinner'),
        ('general', 'General Mess Quality')
    ], default='general', render_kw={'class': 'form-select'})
    comments = TextAreaField('Your Feedback / Review Comments', validators=[DataRequired()], render_kw={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your feedback on meal quality, hygiene, or service...'})
