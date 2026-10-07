from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func
from app.extensions import db
from app.models import MessMenu, MessReview
from app.forms import MessMenuForm, MessReviewForm
from app.utils.decorators import admin_required
from app.utils.helpers import get_or_create_profile

mess_bp = Blueprint('mess', __name__)

@mess_bp.route('/mess')
@login_required
def mess_menu_view():
    profile = get_or_create_profile(current_user)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    active_day = request.args.get('day', datetime.now().strftime('%A'))
    if active_day not in days:
        active_day = 'Monday'

    menus = MessMenu.query.filter_by(day=active_day).all()
    reviews = MessReview.query.order_by(MessReview.created_at.desc()).limit(15).all()
    avg_rating = db.session.query(func.avg(MessReview.rating)).scalar() or 0.0

    review_form = MessReviewForm()
    menu_form = MessMenuForm(day=active_day)

    return render_template('core/mess_menu.html',
                           profile=profile,
                           days=days,
                           active_day=active_day,
                           menus=menus,
                           reviews=reviews,
                           avg_rating=round(float(avg_rating), 1),
                           review_form=review_form,
                           menu_form=menu_form)


@mess_bp.route('/mess/update', methods=['POST'])
@login_required
@admin_required
def mess_menu_update():
    day = request.form.get('day', '').strip()
    meal_type = request.form.get('meal_type', '').strip()
    items = request.form.get('items', '').strip()
    timing = request.form.get('timing', '').strip()

    if day and meal_type and items:
        menu_item = MessMenu.query.filter_by(day=day, meal_type=meal_type).first()
        if not menu_item:
            menu_item = MessMenu(day=day, meal_type=meal_type, items=items, timing=timing)
            db.session.add(menu_item)
        else:
            menu_item.items = items
            menu_item.timing = timing
        db.session.commit()
        flash(f"Mess menu updated for {day} ({meal_type.title()}).", "success")
    else:
        flash("Please fill in all required fields.", "error")

    return redirect(url_for('mess.mess_menu_view', day=day or 'Monday'))


@mess_bp.route('/mess/review', methods=['POST'])
@login_required
def mess_review_create():
    form = MessReviewForm()
    if form.validate_on_submit():
        review = MessReview(
            student_id=current_user.id,
            rating=form.rating.data,
            meal_type=form.meal_type.data,
            comments=form.comments.data.strip()
        )
        db.session.add(review)
        db.session.commit()
        flash("Thank you! Your mess review has been submitted.", "success")
    else:
        flash("Invalid review input. Please check your rating and comments.", "error")

    return redirect(url_for('mess.mess_menu_view'))
