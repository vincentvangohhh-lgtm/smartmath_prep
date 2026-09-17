from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

# Khởi tạo các Extension
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Khởi tạo Extension với App
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Import Models bên trong hàm để tránh Circular Import
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # Đăng ký Blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.exam import exam_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(exam_bp, url_prefix='/exam')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Tự động tạo bảng DB nếu chưa có
    with app.app_context():
        db.create_all()

    return app
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("Đã khởi tạo bảng trên Neon thành công!")