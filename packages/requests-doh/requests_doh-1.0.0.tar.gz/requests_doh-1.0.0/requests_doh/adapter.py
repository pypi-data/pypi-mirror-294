from requests.adapters import HTTPAdapter
from urllib3.connectionpool import HTTPSConnectionPool
from urllib3.contrib.socks import (
    SOCKSHTTPSConnectionPool, 
    SOCKSHTTPConnectionPool,
)

from .connector.default import (
    DoHHTTPConnection,
    DoHHTTPSConnection,
)

from .cachemanager import set_dns_cache_expire_time

from .connector.proxies import (
    SOCKSConnection,
    SOCKSHTTPSConnection
)

from .resolver import set_dns_provider

__all__ = ('DNSOverHTTPSAdapter',)  

class DNSOverHTTPSAdapter(HTTPAdapter):
    """An DoH (DNS over HTTPS) adapter for :class:`requests.Session`
    
    Parameters
    -----------
    provider: :class:`str`
        A DoH provider
    cache_expire_time: :class:`float`
        Set DNS cache expire time
    **kwargs
        These parameters will be passed to :class:`requests.adapters.HTTPAdapter`
    """
    def __init__(self, provider=None, cache_expire_time=None, **kwargs):
        if provider:
            set_dns_provider(provider)

        if cache_expire_time:
            set_dns_cache_expire_time(cache_expire_time)

        super().__init__(**kwargs)

    def get_connection_with_tls_context(self, *args, **kwargs):
        conn = super().get_connection_with_tls_context(*args, **kwargs)
        if isinstance(conn, SOCKSHTTPSConnectionPool):
            conn.ConnectionCls = SOCKSHTTPSConnection
        elif isinstance(conn, SOCKSHTTPConnectionPool):
            conn.ConnectionCls = SOCKSConnection
        elif isinstance(conn, HTTPSConnectionPool):
            conn.ConnectionCls = DoHHTTPSConnection
        else:
            # HTTP type
            conn.ConnectionCls = DoHHTTPConnection
        return conn