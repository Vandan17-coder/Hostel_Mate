from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.announcements import announcements_bp
from app.routes.complaints import complaints_bp
from app.routes.mess import mess_bp
from app.routes.resources import resources_bp
from app.routes.lost_found import lost_found_bp
from app.routes.admin import admin_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(announcements_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(mess_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(lost_found_bp)
    app.register_blueprint(admin_bp)
