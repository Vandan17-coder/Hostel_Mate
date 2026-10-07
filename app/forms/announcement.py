from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class AnnouncementForm(FlaskForm):
    title = StringField('Notice Title', validators=[DataRequired(), Length(max=200)], render_kw={'class': 'form-control', 'placeholder': 'Announcement Title'})
    category = SelectField('Category', choices=[
        ('general', 'General Notice'),
        ('urgent', 'Urgent / Important'),
        ('maintenance', 'Maintenance Work'),
        ('event', 'Hostel Event')
    ], default='general', render_kw={'class': 'form-select'})
    content = TextAreaField('Content / Notice Details', validators=[DataRequired()], render_kw={'class': 'form-control', 'rows': 4, 'placeholder': 'Details of notice...'})
    is_pinned = BooleanField('Pin this notice to top of dashboard', default=False, render_kw={'class': 'form-check-input', 'id': 'id_is_pinned'})
