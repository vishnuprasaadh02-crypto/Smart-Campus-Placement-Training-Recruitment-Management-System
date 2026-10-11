import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'royal_placement_default_secret_key_change_in_production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder for student resumes
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'resumes')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    
    # Database configuration
    USE_SQLITE = os.environ.get('USE_SQLITE', 'false').lower() in ('true', '1', 't')
    
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'college_placement_db')
    
    @classmethod
    def get_database_uri(cls):
        """Construct database URI with MySQL priority and safe SQLite fallback."""
        if cls.USE_SQLITE:
            sqlite_path = os.path.join(BASE_DIR, 'college_placement.db')
            return f"sqlite:///{sqlite_path}"
        
        # Test MySQL connection parameters
        encoded_password = urllib.parse.quote_plus(cls.MYSQL_PASSWORD)
        mysql_uri = f"mysql+pymysql://{cls.MYSQL_USER}:{encoded_password}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DB}?charset=utf8mb4"
        
        # Try checking if MySQL server is reachable with given credentials
        try:
            import pymysql
            conn = pymysql.connect(
                host=cls.MYSQL_HOST,
                user=cls.MYSQL_USER,
                password=cls.MYSQL_PASSWORD,
                port=int(cls.MYSQL_PORT),
                connect_timeout=2
            )
            # Create DB if it doesn't exist
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{cls.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.close()
            return mysql_uri
        except Exception as e:
            # Fallback smoothly to SQLite so user or test environment runs without crash
            sqlite_path = os.path.join(BASE_DIR, 'college_placement.db')
            return f"sqlite:///{sqlite_path}"

    SQLALCHEMY_DATABASE_URI = None  # Populated dynamically during app creation or class access

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    USE_SQLITE = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'test_college_placement.db')}"
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
