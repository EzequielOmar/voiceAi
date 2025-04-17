class Config:
    SECRET_KEY = "dev"  # Replace for production
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = "prod-secret"  # Use env var in real scenario
