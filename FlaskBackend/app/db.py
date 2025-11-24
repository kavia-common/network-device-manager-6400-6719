from typing import Optional
import os
from flask import current_app
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError
from .config import get_config

_client: Optional[MongoClient] = None


# PUBLIC_INTERFACE
def get_db_client() -> MongoClient:
    """
    Return a singleton MongoClient using the configured MONGO_URI.
    Skips the admin 'ping' when running in tests or when DISABLE_DB_PING=true.
    Raises:
        RuntimeError: if connection fails.
    """
    global _client
    if _client is None:
        cfg = get_config()
        try:
            _client = MongoClient(cfg.MONGO_URI)
            # Trigger a quick server check to fail fast if URI is invalid,
            # but skip during tests or when explicitly disabled via env.
            disable_ping_env = os.getenv("DISABLE_DB_PING", "").lower() == "true"
            testing_flag = False
            try:
                # current_app may not be available outside app context
                testing_flag = bool(current_app and current_app.config.get("TESTING"))
            except Exception:
                testing_flag = False
            if not disable_ping_env and not testing_flag:
                _client.admin.command("ping")
        except Exception as exc:
            raise RuntimeError(f"Failed to connect to MongoDB: {exc}") from exc
    return _client


# PUBLIC_INTERFACE
def get_devices_collection():
    """
    Return the MongoDB collection for devices, ensuring a unique index on 'name'.
    Raises:
        RuntimeError: if any DB operation fails.
    """
    try:
        cfg = get_config()
        client = get_db_client()
        db = client[cfg.DB_NAME]
        col = db[cfg.COLLECTION_NAME]
        # Ensure unique index on name for idempotent enforcement
        col.create_index([("name", ASCENDING)], unique=True, name="uniq_name")
        return col
    except PyMongoError as exc:
        raise RuntimeError(f"DB initialization error: {exc}") from exc
