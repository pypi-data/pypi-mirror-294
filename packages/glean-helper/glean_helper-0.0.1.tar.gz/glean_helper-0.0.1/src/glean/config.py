from pydantic import HttpUrl, SecretStr, model_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from functools import wraps
from typing import Optional, Callable
from functools import lru_cache
from dataclasses import dataclass
from datetime import datetime
import logging

class OutputType(str, Enum):
    API = 'api'
    CSV = 'csv'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s: %(message)s', datefmt='%b %d %H:%M:%S %Z')

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')

    # Glean settings
    GLEAN_BACKEND_DOMAIN: Optional[str] = None
    GLEAN_INDEXING_API_KEY: Optional[SecretStr] = None
    GLEAN_CLIENT_API_KEY: Optional[SecretStr] = None

    # Application settings
    OUTPUT_TYPE: OutputType = OutputType.API
    BATCH_SIZE: int = 250

    # Debug and test settings
    DEBUG_MODE: bool = False

    @model_validator(mode='after')
    def validate_settings(self):
        self._validate_glean_settings()
        return self

    def _validate_glean_settings(self):
        pass

@lru_cache
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        for error in e.errors():
            if 'ctx' in error and 'error' in error['ctx']:
                logger.error(error['ctx']['error'])
            else:
                logger.error(error['msg'])
        raise ConfigurationError("Settings validation failed. Please check the configuration.")

def check_api_key(key: str) -> Callable:
    """
    Decorator factory to check if the appropriate Glean API key has been set before executing the method.
    
    Args:
        key (str): The key to check for in the settings. Can be either 'index', 'client', 'both'.
            - 'index' requires GLEAN_INDEXING_API_KEY to be set.
            - 'client' requires GLEAN_CLIENT_API_KEY to be set.
            - 'both' requires both keys to be set.
    
    Returns:
        Callable: The decorator function.
    
    Usage:
        @check_api_key('index')
        def some_method(self):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            settings = get_settings()
            if key == 'index':
                if not settings.GLEAN_INDEXING_API_KEY:
                    raise ConfigurationError("This endpoint requires a Glean Indexing API key which has not been set. Please set GLEAN_INDEXING_API_KEY in your environment or .env file (export GLEAN_INDEXING_API_KEY=your_api_key)")
            elif key == 'client':
                if not settings.GLEAN_CLIENT_API_KEY:
                    raise ConfigurationError("This endpoint requires a Glean Client API key which has not been set. Please set GLEAN_CLIENT_API_KEY in your environment or .env file (export GLEAN_CLIENT_API_KEY=your_api_key)")
            else:  # 'both'
                if not settings.GLEAN_INDEXING_API_KEY:
                    raise ConfigurationError("This endpoint requires both a Glean Indexing API & Client API key to function. The INDEXING API key has not been set. Please set GLEAN_INDEXING_API_KEY in your environment or .env file (export GLEAN_INDEXING_API_KEY=your_api_key)")
                if not settings.GLEAN_CLIENT_API_KEY:
                    raise ConfigurationError("This endpoint requires both a Glean Indexing API & Client API key to function. The CLIENT API key has not been set. Please set GLEAN_CLIENT_API_KEY in your environment or .env file (export GLEAN_CLIENT_API_KEY=your_api_key)")
            return func(*args, **kwargs)
        return wrapper
    return decorator

class ConfigurationError(Exception):
    """Custom exception for configuration errors."""
    pass