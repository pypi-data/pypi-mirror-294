from .api.index import IndexAPI
from .api.client import ClientAPI
from typing import Optional
from .config import get_settings, ConfigurationError

class Glean:
    def __init__(self, backend_domain: Optional[str] = None):
        if backend_domain:
            self.backend_domain = backend_domain
        else:
            settings = get_settings()
            if not settings.GLEAN_BACKEND_DOMAIN:
                raise ConfigurationError('The Glean backend domain has not been set, e.g. companyname-be.glean.com. Please set GLEAN_BACKEND_DOMAIN in your environment or .env file (export GLEAN_BACKEND_DOMAIN=companyname-be.glean.com)')
            
            self.backend_domain = settings.GLEAN_BACKEND_DOMAIN

        print(f"Using backend domain: {self.backend_domain}")
            
        self.index = IndexAPI(backend_domain=self.backend_domain)
        self.client = ClientAPI(backend_domain=self.backend_domain)