import os
from flask import Flask, render_template
from config import config_by_name, Config
from extensions import db, login_manager
from routes import (
    auth_bp, admin_bp, students_bp, companies_bp, jobs_bp,
    applications_bp, interviews_bp, training_bp, placements_bp,
    reports_bp, notifications_bp, errors_bp
)
from models import User, Notification
from flask_login import current_user

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    config_class = config_by_name.get(config_name, Config)
    app.config.from_object(config_class)

    # Resolve dynamic Database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = config_class.get_database_uri()

    # Ensure uploads directory exists
    os.makedirs(app.config.get('UPLOAD_FOLDER', os.path.join(app.root_path, 'uploads', 'resumes')), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(interviews_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(placements_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(errors_bp)

    # Global context processors for templates
    @app.context_processor
    def inject_global_context():
        unread_count = 0
        if current_user.is_authenticated:
            try:
                unread_count = Notification.query.filter_by(user_id=current_user.user_id, is_read=False).count()
            except Exception:
                unread_count = 0
        return {
            'unread_notifications_count': unread_count,
            'app_name': 'ROYAL PLACEMENT',
            'app_subtitle': 'College Placement & Recruitment Portal'
        }

    # Custom Jinja filters
    @app.template_filter('currency_lpa')
    def currency_lpa_filter(val):
        try:
            return f"₹{float(val):.2f} LPA"
        except (ValueError, TypeError):
            return f"₹{val} LPA"

    @app.template_filter('format_date')
    def format_date_filter(val, fmt='%d %b %Y'):
        if not val:
            return ''
        try:
            return val.strftime(fmt)
        except Exception:
            return str(val)

    # Create tables automatically on startup if not present
    with app.app_context():
        try:
            db.create_all()
            _bootstrap_admin_if_needed()
        except Exception as e:
            app.logger.warning(f"Database initialization note: {e}")

    return app

def _bootstrap_admin_if_needed():
    """Ensures at least one administrator account exists."""
    from models import User
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_user = User(
            username='admin',
            email='admin@royalplacement.edu',
            role='admin',
            is_active=True
        )
        admin_user.set_password('Admin@123')
        db.session.add(admin_user)
        db.session.commit()

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
