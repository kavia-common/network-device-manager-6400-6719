import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """
    Application configuration loaded from environment variables.

    Environment variables:
    - MONGO_URI: MongoDB connection string (e.g., mongodb://localhost:27017)
    - DB_NAME: Database name to use (default: "network_device_manager")
    - COLLECTION_NAME: Collection name for devices (default: "devices")
    """
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "network_device_manager")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "devices")


# PUBLIC_INTERFACE
def get_config() -> Config:
    """Return the immutable Config object with all application settings."""
    return Config()
