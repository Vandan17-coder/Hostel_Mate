from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.extensions import db
from app.models import User, UserProfile
from app.forms import AdminStudentEditForm
from app.utils.decorators import admin_required
from app.utils.helpers import get_or_create_profile

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin-students')
@login_required
@admin_required
def admin_students_list():
    profile = get_or_create_profile(current_user)
    query = request.args.get('q', '').strip()
    block_filter = request.args.get('block', '').strip()

    stmt = UserProfile.query.join(User)

    if query:
        stmt = stmt.filter(or_(
            User.username.ilike(f"%{query}%"),
            User.first_name.ilike(f"%{query}%"),
            User.last_name.ilike(f"%{query}%"),
            UserProfile.roll_number.ilike(f"%{query}%"),
            UserProfile.room_number.ilike(f"%{query}%")
        ))
    if block_filter:
        stmt = stmt.filter(UserProfile.hostel_block == block_filter)

    students = stmt.all()

    return render_template('core/admin_students.html',
                           profile=profile,
                           students=students,
                           query=query,
                           block_filter=block_filter)


@admin_bp.route('/admin-students/<int:pk>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_student_edit(pk):
    profile = get_or_create_profile(current_user)
    target_profile = UserProfile.query.get_or_404(pk)

    if request.method == 'POST':
        target_profile.roll_number = request.form.get('roll_number', '').strip() or None
        target_profile.room_number = request.form.get('room_number', '').strip() or None
        target_profile.hostel_block = request.form.get('hostel_block', 'Block A').strip()
        target_profile.phone = request.form.get('phone', '').strip() or None
        new_role = request.form.get('role', 'student').strip()
        target_profile.role = new_role

        db.session.commit()
        flash(f"Updated student details for {target_profile.user.username}.", "success")
        return redirect(url_for('admin.admin_students_list'))

    return render_template('core/admin_student_edit.html',
                           profile=profile,
                           target_profile=target_profile)
