from datetime import datetime
from app.extensions import db

class MessMenu(db.Model):
    __tablename__ = 'mess_menus'
    __table_args__ = (
        db.UniqueConstraint('day', 'meal_type', name='uq_day_meal_type'),
    )

    DAY_CHOICES = {
        'Monday': 'Monday',
        'Tuesday': 'Tuesday',
        'Wednesday': 'Wednesday',
        'Thursday': 'Thursday',
        'Friday': 'Friday',
        'Saturday': 'Saturday',
        'Sunday': 'Sunday',
    }

    MEAL_CHOICES = {
        'breakfast': 'Breakfast',
        'lunch': 'Lunch',
        'snacks': 'Evening Snacks',
        'dinner': 'Dinner',
    }

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(15), nullable=False)
    meal_type = db.Column(db.String(15), nullable=False)
    items = db.Column(db.Text, nullable=False)
    timing = db.Column(db.String(50), nullable=True, default='')

    def get_meal_type_display(self):
        return self.MEAL_CHOICES.get(self.meal_type, self.meal_type.title())

    def get_day_display(self):
        return self.DAY_CHOICES.get(self.day, self.day)

    def __repr__(self):
        return f"<MessMenu {self.day} - {self.meal_type}>"


class MessReview(db.Model):
    __tablename__ = 'mess_reviews'

    MEAL_CHOICES = {
        'breakfast': 'Breakfast',
        'lunch': 'Lunch',
        'snacks': 'Evening Snacks',
        'dinner': 'Dinner',
        'general': 'General Mess Quality',
    }

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    meal_type = db.Column(db.String(15), default='general', nullable=False)
    comments = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # Relationships
    student = db.relationship('User', back_populates='mess_reviews')

    def get_meal_type_display(self):
        return self.MEAL_CHOICES.get(self.meal_type, self.meal_type.title())

    def __repr__(self):
        return f"<MessReview {self.student_id} ({self.rating}/5)>"
