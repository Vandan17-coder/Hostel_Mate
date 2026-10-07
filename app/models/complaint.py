from datetime import datetime
from app.extensions import db

class Complaint(db.Model):
    __tablename__ = 'complaints'

    CATEGORY_CHOICES = {
        'electrical': 'Electrical',
        'plumbing': 'Plumbing',
        'cleanliness': 'Cleanliness & Hygiene',
        'wifi': 'Wi-Fi & Internet',
        'furniture': 'Furniture & Carpentry',
        'other': 'Other',
    }

    STATUS_CHOICES = {
        'pending': 'Pending',
        'in_progress': 'In Progress',
        'resolved': 'Resolved',
        'rejected': 'Rejected',
    }

    PRIORITY_CHOICES = {
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High',
    }

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    hostel_block = db.Column(db.String(50), default='Block A', nullable=False)
    priority = db.Column(db.String(10), default='medium', nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    admin_remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    student = db.relationship('User', back_populates='complaints')

    def get_category_display(self):
        return self.CATEGORY_CHOICES.get(self.category, self.category.title())

    def get_status_display(self):
        return self.STATUS_CHOICES.get(self.status, self.status.title())

    def get_priority_display(self):
        return self.PRIORITY_CHOICES.get(self.priority, self.priority.title())

    def __repr__(self):
        return f"<Complaint #{self.id} {self.title} ({self.status})>"
