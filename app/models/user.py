from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(254), nullable=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_staff = db.Column(db.Boolean, default=False, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # Relationships
    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    announcements = db.relationship('Announcement', back_populates='author', lazy='dynamic', cascade='all, delete-orphan')
    complaints = db.relationship('Complaint', back_populates='student', lazy='dynamic', cascade='all, delete-orphan')
    mess_reviews = db.relationship('MessReview', back_populates='student', lazy='dynamic', cascade='all, delete-orphan')
    resources = db.relationship('Resource', back_populates='uploader', lazy='dynamic', cascade='all, delete-orphan')
    lost_and_found_items = db.relationship('LostAndFound', back_populates='reporter', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        full = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full if full else self.username

    def __repr__(self):
        return f"<User {self.username}>"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    ROLE_CHOICES = {
        'student': 'Student',
        'admin': 'Hostel Admin / Warden',
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    role = db.Column(db.String(10), default='student', nullable=False)
    roll_number = db.Column(db.String(20), nullable=True)
    room_number = db.Column(db.String(20), nullable=True)
    hostel_block = db.Column(db.String(50), default='Block A', nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    emergency_contact = db.Column(db.String(15), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    # Relationships
    user = db.relationship('User', back_populates='profile')

    def is_admin(self):
        return self.role == 'admin' or (self.user and self.user.is_superuser)

    def get_role_display(self):
        return self.ROLE_CHOICES.get(self.role, self.role.title())

    def __repr__(self):
        return f"<UserProfile {self.user.username if self.user else self.id} ({self.role})>"
