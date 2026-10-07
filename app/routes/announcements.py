from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.extensions import db
from app.models import Announcement
from app.forms import AnnouncementForm
from app.utils.decorators import admin_required
from app.utils.helpers import get_or_create_profile

announcements_bp = Blueprint('announcements', __name__)

@announcements_bp.route('/announcements')
@login_required
def announcements_list():
    profile = get_or_create_profile(current_user)
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    stmt = Announcement.query
    if query:
        stmt = stmt.filter(or_(
            Announcement.title.ilike(f"%{query}%"),
            Announcement.content.ilike(f"%{query}%")
        ))
    if category:
        stmt = stmt.filter_by(category=category)

    announcements = stmt.order_by(Announcement.is_pinned.desc(), Announcement.created_at.desc()).all()
    form = AnnouncementForm()

    return render_template('core/announcements.html',
                           profile=profile,
                           announcements=announcements,
                           form=form,
                           query=query,
                           selected_category=category)


@announcements_bp.route('/announcements/create', methods=['POST'])
@login_required
@admin_required
def announcement_create():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data.strip(),
            category=form.category.data,
            content=form.content.data.strip(),
            is_pinned=bool(form.is_pinned.data),
            created_by_id=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()
        flash("Announcement posted successfully!", "success")
    else:
        flash("Failed to post announcement. Check inputs.", "error")
    return redirect(url_for('announcements.announcements_list'))


@announcements_bp.route('/announcements/delete/<int:pk>', methods=['GET', 'POST'])
@login_required
@admin_required
def announcement_delete(pk):
    announcement = Announcement.query.get_or_404(pk)
    db.session.delete(announcement)
    db.session.commit()
    flash("Announcement deleted successfully.", "success")
    return redirect(url_for('announcements.announcements_list'))
