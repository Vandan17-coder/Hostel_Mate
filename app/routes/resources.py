from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.extensions import db
from app.models import Resource
from app.forms import ResourceForm
from app.utils.helpers import get_or_create_profile

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/resources')
@login_required
def resources_list():
    profile = get_or_create_profile(current_user)
    category_filter = request.args.get('category', '').strip()
    query = request.args.get('q', '').strip()

    stmt = Resource.query
    if category_filter:
        stmt = stmt.filter_by(category=category_filter)
    if query:
        stmt = stmt.filter(or_(
            Resource.title.ilike(f"%{query}%"),
            Resource.description.ilike(f"%{query}%")
        ))

    resources = stmt.order_by(Resource.created_at.desc()).all()
    form = ResourceForm()

    return render_template('core/resources.html',
                           profile=profile,
                           resources=resources,
                           form=form,
                           category_filter=category_filter,
                           query=query)


@resources_bp.route('/resources/create', methods=['POST'])
@login_required
def resource_create():
    form = ResourceForm()
    if form.validate_on_submit():
        res = Resource(
            uploader_id=current_user.id,
            title=form.title.data.strip(),
            category=form.category.data,
            description=form.description.data.strip(),
            contact_info=form.contact_info.data.strip(),
            is_available=True
        )
        db.session.add(res)
        db.session.commit()
        flash("Resource shared successfully with hostel mates!", "success")
    else:
        flash("Error sharing resource. Please check the form.", "error")

    return redirect(url_for('resources.resources_list'))


@resources_bp.route('/resources/<int:pk>/toggle', methods=['GET', 'POST'])
@login_required
def resource_toggle_status(pk):
    profile = get_or_create_profile(current_user)
    resource = Resource.query.get_or_404(pk)

    if resource.uploader_id != current_user.id and not profile.is_admin():
        flash("Permission denied.", "error")
        return redirect(url_for('resources.resources_list'))

    resource.is_available = not resource.is_available
    db.session.commit()
    status_str = "Available" if resource.is_available else "Borrowed / Unavailable"
    flash(f"Resource state changed to '{status_str}'.", "success")

    return redirect(url_for('resources.resources_list'))


@resources_bp.route('/resources/<int:pk>/delete', methods=['GET', 'POST'])
@login_required
def resource_delete(pk):
    profile = get_or_create_profile(current_user)
    resource = Resource.query.get_or_404(pk)

    if resource.uploader_id != current_user.id and not profile.is_admin():
        flash("Permission denied.", "error")
        return redirect(url_for('resources.resources_list'))

    db.session.delete(resource)
    db.session.commit()
    flash("Resource removed.", "success")

    return redirect(url_for('resources.resources_list'))
