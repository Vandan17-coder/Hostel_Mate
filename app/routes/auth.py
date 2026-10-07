from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User, UserProfile
from app.forms import UserRegisterForm, LoginForm, ProfileUpdateForm
from app.utils.helpers import get_or_create_profile

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = UserRegisterForm()
    if form.validate_on_submit():
        # Check if username exists
        existing_user = User.query.filter_by(username=form.username.data.strip()).first()
        if existing_user:
            flash("Username already exists. Please choose another.", "error")
            return render_template('core/register.html', form=form)

        user = User(
            username=form.username.data.strip(),
            first_name=form.first_name.data.strip() if form.first_name.data else '',
            last_name=form.last_name.data.strip() if form.last_name.data else '',
            email=form.email.data.strip() if form.email.data else ''
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        role = form.role.data or 'student'
        profile = UserProfile(
            user_id=user.id,
            role=role,
            roll_number=form.roll_number.data.strip() if form.roll_number.data else None,
            room_number=form.room_number.data.strip() if form.room_number.data else None,
            hostel_block=form.hostel_block.data.strip() if form.hostel_block.data else 'Block A',
            phone=form.phone.data.strip() if form.phone.data else None
        )
        db.session.add(profile)
        db.session.commit()

        login_user(user)
        flash(f"Welcome to HostelMate, {user.username}! Account created successfully.", "success")
        return redirect(url_for('main.dashboard'))
    elif request.method == 'POST':
        flash("Registration failed. Please correct the errors below.", "error")

    return render_template('core/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            get_or_create_profile(user)
            flash(f"Logged in successfully as {user.username}.", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash("Invalid username or password.", "error")
    elif request.method == 'POST':
        flash("Please fill in all required fields.", "error")

    return render_template('core/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_prof = get_or_create_profile(current_user)
    form = ProfileUpdateForm(obj=user_prof)

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()

        if form.validate_on_submit():
            user_prof.roll_number = form.roll_number.data.strip() if form.roll_number.data else None
            user_prof.room_number = form.room_number.data.strip() if form.room_number.data else None
            user_prof.hostel_block = form.hostel_block.data.strip() if form.hostel_block.data else 'Block A'
            user_prof.phone = form.phone.data.strip() if form.phone.data else None
            user_prof.emergency_contact = form.emergency_contact.data.strip() if form.emergency_contact.data else None
            user_prof.bio = form.bio.data.strip() if form.bio.data else None

            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email

            db.session.commit()
            flash("Your profile details have been updated successfully!", "success")
            return redirect(url_for('auth.profile'))
        else:
            flash("Please check the form for errors.", "error")
    else:
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email

    return render_template('core/profile.html', profile=user_prof, form=form, user=current_user)
