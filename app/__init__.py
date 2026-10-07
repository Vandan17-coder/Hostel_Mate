import os
from flask import Flask, url_for as flask_url_for
from flask_login import current_user
from config import config_by_name
from app.extensions import db, migrate, login_manager, csrf
from app.utils.filters import register_filters
from app.routes import register_blueprints
from app.utils.helpers import get_or_create_profile

def smart_url_for(endpoint, **values):
    """Support both direct route names and blueprint names for Jinja templates."""
    alias_map = {
        'dashboard': 'main.dashboard',
        'login': 'auth.login',
        'register': 'auth.register',
        'logout': 'auth.logout',
        'profile': 'auth.profile',
        'announcements': 'announcements.announcements_list',
        'announcement_create': 'announcements.announcement_create',
        'announcement_delete': 'announcements.announcement_delete',
        'complaints': 'complaints.complaints_list',
        'complaint_create': 'complaints.complaint_create',
        'complaint_detail': 'complaints.complaint_detail',
        'complaint_update_status': 'complaints.complaint_update_status',
        'mess_menu': 'mess.mess_menu_view',
        'mess_menu_update': 'mess.mess_menu_update',
        'mess_review_create': 'mess.mess_review_create',
        'resources': 'resources.resources_list',
        'resource_create': 'resources.resource_create',
        'resource_toggle_status': 'resources.resource_toggle_status',
        'resource_delete': 'resources.resource_delete',
        'lost_found': 'lost_found.lost_found_list',
        'lost_found_create': 'lost_found.lost_found_create',
        'lost_found_toggle_status': 'lost_found.lost_found_toggle_status',
        'lost_found_delete': 'lost_found.lost_found_delete',
        'admin_students': 'admin.admin_students_list',
        'admin_student_edit': 'admin.admin_student_edit',
    }
    target = alias_map.get(endpoint, endpoint)
    return flask_url_for(target, **values)

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Ensure instance directory exists for SQLite
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register Jinja Filters
    register_filters(app)

    # Register Blueprints
    register_blueprints(app)

    # Context Processors
    @app.context_processor
    def inject_globals():
        prof = None
        if current_user.is_authenticated:
            try:
                prof = get_or_create_profile(current_user)
            except Exception:
                pass
        return {
            'user': current_user,
            'current_user': current_user,
            'profile': prof,
            'url_for': smart_url_for
        }

    # Register CLI seed command
    from app.commands import register_commands
    register_commands(app)

    return app
