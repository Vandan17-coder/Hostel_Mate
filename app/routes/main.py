from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from app.extensions import db
from app.models import UserProfile, Announcement, Complaint, MessMenu, MessReview, Resource, LostAndFound
from app.utils.helpers import get_or_create_profile

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    profile = get_or_create_profile(current_user)

    if profile.is_admin():
        # Admin / Warden Analytics
        total_students = UserProfile.query.filter_by(role='student').count()
        total_complaints = Complaint.query.count()
        pending_complaints = Complaint.query.filter_by(status='pending').count()
        in_progress_complaints = Complaint.query.filter_by(status='in_progress').count()
        resolved_complaints = Complaint.query.filter_by(status='resolved').count()
        total_resources = Resource.query.filter_by(is_available=True).count()
        open_lost_found = LostAndFound.query.filter_by(status='open').count()

        avg_rating = db.session.query(func.avg(MessReview.rating)).scalar() or 0.0

        recent_complaints = Complaint.query.order_by(Complaint.created_at.desc()).limit(5).all()
        recent_announcements = Announcement.query.order_by(Announcement.is_pinned.desc(), Announcement.created_at.desc()).limit(4).all()

        context = {
            'profile': profile,
            'is_admin_dashboard': True,
            'total_students': total_students,
            'total_complaints': total_complaints,
            'pending_complaints': pending_complaints,
            'in_progress_complaints': in_progress_complaints,
            'resolved_complaints': resolved_complaints,
            'total_resources': total_resources,
            'open_lost_found': open_lost_found,
            'avg_rating': round(float(avg_rating), 1),
            'recent_complaints': recent_complaints,
            'recent_announcements': recent_announcements,
        }
        return render_template('core/dashboard_admin.html', **context)
    else:
        # Student Dashboard
        today_day = datetime.now().strftime('%A')
        my_complaints = Complaint.query.filter_by(student_id=current_user.id).order_by(Complaint.created_at.desc()).limit(5).all()
        pinned_announcements = Announcement.query.filter_by(is_pinned=True).order_by(Announcement.created_at.desc()).limit(3).all()
        latest_announcements = Announcement.query.filter_by(is_pinned=False).order_by(Announcement.created_at.desc()).limit(4).all()
        today_mess_menu = MessMenu.query.filter_by(day=today_day).all()
        recent_resources = Resource.query.filter_by(is_available=True).order_by(Resource.created_at.desc()).limit(4).all()
        recent_lost_found = LostAndFound.query.filter_by(status='open').order_by(LostAndFound.created_at.desc()).limit(4).all()

        context = {
            'profile': profile,
            'is_admin_dashboard': False,
            'today_day': today_day,
            'my_complaints': my_complaints,
            'pinned_announcements': pinned_announcements,
            'latest_announcements': latest_announcements,
            'today_mess_menu': today_mess_menu,
            'recent_resources': recent_resources,
            'recent_lost_found': recent_lost_found,
        }
        return render_template('core/dashboard_student.html', **context)
