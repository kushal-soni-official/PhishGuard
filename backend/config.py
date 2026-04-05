import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_super_secret_phishguard_key')
    DEBUG = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16MB max upload
