from app.extensions import db
from app.models.user import UserProfile

def get_or_create_profile(user):
    """Utility to ensure UserProfile exists for every user."""
    profile = UserProfile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = UserProfile(user_id=user.id, role='admin' if user.is_superuser else 'student')
        db.session.add(profile)
        db.session.commit()
    elif user.is_superuser and profile.role != 'admin':
        profile.role = 'admin'
        db.session.commit()
    return profile
