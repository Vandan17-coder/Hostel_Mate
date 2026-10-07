from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.extensions import db
from app.models import LostAndFound
from app.forms import LostAndFoundForm
from app.utils.helpers import get_or_create_profile

lost_found_bp = Blueprint('lost_found', __name__)

@lost_found_bp.route('/lost-found')
@login_required
def lost_found_list():
    profile = get_or_create_profile(current_user)
    type_filter = request.args.get('type', '').strip()
    status_filter = request.args.get('status', '').strip()
    query = request.args.get('q', '').strip()

    stmt = LostAndFound.query
    if type_filter:
        stmt = stmt.filter_by(item_type=type_filter)
    if status_filter:
        stmt = stmt.filter_by(status=status_filter)
    if query:
        stmt = stmt.filter(or_(
            LostAndFound.title.ilike(f"%{query}%"),
            LostAndFound.description.ilike(f"%{query}%"),
            LostAndFound.location.ilike(f"%{query}%")
        ))

    items = stmt.order_by(LostAndFound.created_at.desc()).all()
    form = LostAndFoundForm()

    return render_template('core/lost_found.html',
                           profile=profile,
                           items=items,
                           form=form,
                           type_filter=type_filter,
                           status_filter=status_filter,
                           query=query)


@lost_found_bp.route('/lost-found/create', methods=['POST'])
@login_required
def lost_found_create():
    form = LostAndFoundForm()
    if form.validate_on_submit():
        lf_item = LostAndFound(
            reported_by_id=current_user.id,
            item_type=form.item_type.data,
            title=form.title.data.strip(),
            category=form.category.data.strip() if form.category.data else 'Personal Belongings',
            location=form.location.data.strip(),
            date_event=form.date_event.data,
            contact_info=form.contact_info.data.strip(),
            description=form.description.data.strip(),
            status='open'
        )
        db.session.add(lf_item)
        db.session.commit()
        flash(f"Item reported as {lf_item.get_item_type_display()} successfully!", "success")
    else:
        flash("Error submitting Lost & Found report. Please check the form.", "error")

    return redirect(url_for('lost_found.lost_found_list'))


@lost_found_bp.route('/lost-found/<int:pk>/toggle', methods=['GET', 'POST'])
@login_required
def lost_found_toggle_status(pk):
    profile = get_or_create_profile(current_user)
    item = LostAndFound.query.get_or_404(pk)

    if item.reported_by_id != current_user.id and not profile.is_admin():
        flash("Permission denied.", "error")
        return redirect(url_for('lost_found.lost_found_list'))

    item.status = 'resolved' if item.status == 'open' else 'open'
    db.session.commit()
    flash(f"Item marked as {item.get_status_display()}.", "success")

    return redirect(url_for('lost_found.lost_found_list'))


@lost_found_bp.route('/lost-found/<int:pk>/delete', methods=['GET', 'POST'])
@login_required
def lost_found_delete(pk):
    profile = get_or_create_profile(current_user)
    item = LostAndFound.query.get_or_404(pk)

    if item.reported_by_id != current_user.id and not profile.is_admin():
        flash("Permission denied.", "error")
        return redirect(url_for('lost_found.lost_found_list'))

    db.session.delete(item)
    db.session.commit()
    flash("Item deleted.", "success")

    return redirect(url_for('lost_found.lost_found_list'))
