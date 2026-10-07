from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.extensions import db
from app.models import Complaint
from app.forms import ComplaintForm, ComplaintStatusForm
from app.utils.decorators import admin_required
from app.utils.helpers import get_or_create_profile

complaints_bp = Blueprint('complaints', __name__)

@complaints_bp.route('/complaints')
@login_required
def complaints_list():
    profile = get_or_create_profile(current_user)
    status_filter = request.args.get('status', '').strip()
    category_filter = request.args.get('category', '').strip()
    query = request.args.get('q', '').strip()

    if profile.is_admin():
        stmt = Complaint.query
    else:
        stmt = Complaint.query.filter_by(student_id=current_user.id)

    if status_filter:
        stmt = stmt.filter_by(status=status_filter)
    if category_filter:
        stmt = stmt.filter_by(category=category_filter)
    if query:
        stmt = stmt.filter(or_(
            Complaint.title.ilike(f"%{query}%"),
            Complaint.description.ilike(f"%{query}%"),
            Complaint.room_number.ilike(f"%{query}%")
        ))

    complaints = stmt.order_by(Complaint.created_at.desc()).all()

    form = ComplaintForm(
        room_number=profile.room_number or '',
        hostel_block=profile.hostel_block or 'Block A'
    )

    return render_template('core/complaints.html',
                           profile=profile,
                           complaints=complaints,
                           form=form,
                           status_filter=status_filter,
                           category_filter=category_filter,
                           query=query)


@complaints_bp.route('/complaints/create', methods=['POST'])
@login_required
def complaint_create():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(
            student_id=current_user.id,
            title=form.title.data.strip(),
            category=form.category.data,
            priority=form.priority.data,
            room_number=form.room_number.data.strip(),
            hostel_block=form.hostel_block.data.strip(),
            description=form.description.data.strip(),
            status='pending'
        )
        db.session.add(complaint)
        db.session.commit()
        flash("Complaint submitted successfully! Warden will review it shortly.", "success")
    else:
        flash("Failed to submit complaint. Check your input.", "error")
    return redirect(url_for('complaints.complaints_list'))


@complaints_bp.route('/complaints/<int:pk>')
@login_required
def complaint_detail(pk):
    profile = get_or_create_profile(current_user)
    complaint = Complaint.query.get_or_404(pk)

    # Permission check
    if not profile.is_admin() and complaint.student_id != current_user.id:
        flash("Permission denied.", "error")
        return redirect(url_for('complaints.complaints_list'))

    return render_template('core/complaint_detail.html',
                           profile=profile,
                           complaint=complaint)


@complaints_bp.route('/complaints/<int:pk>/status', methods=['POST'])
@login_required
@admin_required
def complaint_update_status(pk):
    complaint = Complaint.query.get_or_404(pk)
    new_status = request.form.get('status', '').strip()
    admin_remarks = request.form.get('admin_remarks', '').strip()

    if new_status in Complaint.STATUS_CHOICES:
        complaint.status = new_status
        complaint.admin_remarks = admin_remarks
        db.session.commit()
        flash(f"Complaint #{complaint.id} status updated to {complaint.get_status_display()}.", "success")
    else:
        flash("Invalid status selected.", "error")

    return redirect(url_for('complaints.complaint_detail', pk=pk))
