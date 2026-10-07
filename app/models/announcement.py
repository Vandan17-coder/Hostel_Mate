from datetime import datetime
from app.extensions import db

class Announcement(db.Model):
    __tablename__ = 'announcements'

    CATEGORY_CHOICES = {
        'general': 'General Notice',
        'urgent': 'Urgent / Important',
        'maintenance': 'Maintenance Work',
        'event': 'Hostel Event',
    }

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), default='general', nullable=False)
    is_pinned = db.Column(db.Boolean, default=False, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    author = db.relationship('User', back_populates='announcements')

    # Alias for template backwards compatibility
    @property
    def created_by(self):
        return self.author

    def get_category_display(self):
        return self.CATEGORY_CHOICES.get(self.category, self.category.title())

    def __repr__(self):
        return f"<Announcement {self.title}>"
