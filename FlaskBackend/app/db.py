from typing import Optional
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError
from .config import get_config

_client: Optional[MongoClient] = None


# PUBLIC_INTERFACE
def get_db_client() -> MongoClient:
    """
    Return a singleton MongoClient using the configured MONGO_URI.
    Raises:
        RuntimeError: if connection fails.
    """
    global _client
    if _client is None:
        cfg = get_config()
        try:
            _client = MongoClient(cfg.MONGO_URI)
            # Trigger a quick server check to fail fast if URI is invalid
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
