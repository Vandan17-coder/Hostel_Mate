from datetime import datetime
from app.extensions import db

class Resource(db.Model):
    __tablename__ = 'resources'

    CATEGORY_CHOICES = {
        'book': 'Books & Notes',
        'electronics': 'Electronics & Accessories',
        'sports': 'Sports Goods',
        'lab': 'Lab & Study Tools',
        'other': 'Other Utility',
    }

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), default='book', nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # Relationships
    uploader = db.relationship('User', back_populates='resources')

    def get_category_display(self):
        return self.CATEGORY_CHOICES.get(self.category, self.category.title())

    def __repr__(self):
        return f"<Resource {self.title}>"


class LostAndFound(db.Model):
    __tablename__ = 'lost_and_found'

    TYPE_CHOICES = {
        'lost': 'Lost Item',
        'found': 'Found Item',
    }

    STATUS_CHOICES = {
        'open': 'Open / Searching',
        'resolved': 'Claimed / Resolved',
    }

    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='Personal Belongings', nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    date_event = db.Column(db.Date, nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(15), default='open', nullable=False)
    reported_by_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # Relationships
    reporter = db.relationship('User', back_populates='lost_and_found_items')

    # Alias for template backwards compatibility
    @property
    def reported_by(self):
        return self.reporter

    def get_item_type_display(self):
        return self.TYPE_CHOICES.get(self.item_type, self.item_type.title())

    def get_status_display(self):
        return self.STATUS_CHOICES.get(self.status, self.status.title())

    def __repr__(self):
        return f"<LostAndFound [{self.item_type}] {self.title}>"
