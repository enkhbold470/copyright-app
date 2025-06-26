import os
from pathlib import Path

class Config:
    """Base configuration"""
    
    def __init__(self):
        # Load environment variables from .env file if it exists
        self.load_env_file()
    
    def load_env_file(self):
        """Load environment variables from .env file"""
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key] = value
    
    @property
    def SECRET_KEY(self):
        return os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    
    @property
    def DEBUG(self):
        return os.getenv('DEBUG', 'true').lower() == 'true'
    
    @property
    def HOST(self):
        return os.getenv('HOST', '0.0.0.0')
    
    @property
    def PORT(self):
        return int(os.getenv('PORT', 8080))
    
    @property
    def ENV(self):
        return os.getenv('ENV', 'development')
    
    @property
    def MAX_CONTENT_LENGTH(self):
        return int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    
    @property
    def UPLOAD_FOLDER(self):
        return os.getenv('UPLOAD_FOLDER', 'uploads')
    
    @property
    def OUTPUT_FOLDER(self):
        return os.getenv('OUTPUT_FOLDER', 'output')

# Create global config instance
config = Config() 