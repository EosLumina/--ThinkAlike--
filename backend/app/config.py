class Config:
    """
    Configuration class for the backend application.
    Loads configuration settings from environment variables or defaults.
    """
    DEBUG = False  # Debug mode (default: False)
    SECRET_KEY = "your-default-secret-key"  # Replace with a strong secret key in production!

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///thinkalike.db"  # SQLite database URL for development
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance

    # API Keys and External Service Credentials
    AI_API_KEY = "your-default-ai-api-key"  # Placeholder for an AI service API key

    # Application-Specific Configuration
    UI_URL = "http://localhost:3000"  # URL of the UI application

config = Config()