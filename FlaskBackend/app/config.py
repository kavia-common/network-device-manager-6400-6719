import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """
    Application configuration loaded from environment variables with sensible defaults
    so the service can run out-of-the-box without a .env file.

    Environment variables (defaults shown):
    - MONGO_URI: MongoDB connection string (default: "mongodb://localhost:27017")
    - DB_NAME: Database name to use (default: "network_device_manager")
    - COLLECTION_NAME: Collection name for devices (default: "devices")
    """
    # Defaults enable running locally without providing env vars
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb+srv://db_user:vettel%402012@cluster0.htz84wq.mongodb.net/network?retryWrites=true&w=majority")
    DB_NAME: str = os.getenv("DB_NAME", "network_device_manager")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "devices")


# PUBLIC_INTERFACE
def get_config() -> Config:
    """Return the immutable Config object with all application settings."""
    return Config()
