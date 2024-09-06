import httpx
import asyncio
import logging
from typing import Optional
from cachetools import cached, TTLCache

# Version
__version__ = "2024.1009-alpha"

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)

# Create a cache for API responses (optional)
# Cache up to 100 items with a 5-minute TTL
cache = TTLCache(maxsize=100, ttl=300)


class WatchYourLANClient:
    def __init__(self, base_url: str = "http://localhost:8840", async_mode: bool = True, verify_ssl: bool = True,
                 timeout: float = 10.0, headers: Optional[dict] = {}, retries: int = 3):
        """
        Initializes the API client.

        :param base_url: Base URL of the API (default: http://localhost:8840)
        :param async_mode: Boolean to choose async or sync mode (default: True)
        :param verify_ssl: Boolean to verify SSL certificates or not (default: True)
        :param timeout: Timeout for HTTP requests (default: 10 seconds)
        :param headers: Optional headers to send with each request (default: None)
        :param retries: Number of retry attempts in case of failure (default: 3)
        """
        self.base_url = base_url
        self.async_mode = async_mode
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.retries = retries
        # Add on default headers
        self.headers = dict({
            "User-Agent": "WatchYourLANClient/1.0",
            "Accept": "application/json",
        }, **headers)

        if self.async_mode:
            self.client = httpx.AsyncClient(
                base_url=self.base_url, verify=self.verify_ssl, timeout=self.timeout, headers=self.headers)
        else:
            self.client = httpx.Client(
                base_url=self.base_url, verify=self.verify_ssl, timeout=self.timeout, headers=self.headers)

    async def close(self):
        """ Close the client connection for async mode. """
        if self.async_mode:
            await self.client.aclose()

    def close_sync(self):
        """ Close the client connection for sync mode. """
        if not self.async_mode:
            self.client.close()

    def _run(self, coroutine):
        """ Helper method to run async code in sync mode using asyncio. """
        return asyncio.run(coroutine) if not asyncio.get_event_loop().is_running() else asyncio.create_task(coroutine)

    def _request(self, method: str, url: str, params: Optional[dict] = None, retries: Optional[int] = None, **kwargs):
        """
        Helper method to perform HTTP requests.
        Handles both async and sync modes with retry logic and error handling.
        """
        retries = retries or self.retries

        attempts = 0
        while attempts < retries:
            try:
                if self.async_mode:
                    async def async_request():
                        response = await self.client.request(method, url, params=params, **kwargs)
                        response.raise_for_status()
                        logging.info(f"Received response: {response.json()}")
                        return response.json()
                    return self._run(async_request())
                else:
                    response = self.client.request(
                        method, url, params=params, **kwargs)
                    response.raise_for_status()
                    logging.info(f"Received response: {response.json()}")
                    return response.json()
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                attempts += 1
                if attempts >= retries:
                    logging.error(f"Failed after {retries} attempts: {e}")
                    raise Exception(f"Failed after {retries} attempts: {e}")
                logging.warning(
                    f"Retrying request ({attempts}/{retries}) after error: {e}")

    # Unified API Methods for both Sync/Async modes
    @cached(cache)  # Optional caching to reduce repeated requests
    def _get_all_hosts_cached(self):
        """
        Get all hosts with caching.
        GET /api/all
        """
        return self._request("GET", "/api/all")

    def get_all_hosts(self, bypass_cache: bool = False):
        """
        Get all hosts. Optionally bypass the cache.
        :param bypass_cache: Boolean to bypass the cache (default: False).
        """
        if bypass_cache:
            logging.info("Bypassing cache for 'get_all_hosts' request.")
            return self._request("GET", "/api/all")
        return self._get_all_hosts_cached()

    def get_host_history(self, mac: str = ""):
        """
        Get host history.
        GET /api/history/{mac}
        :param mac: MAC address of the host (optional).
        """
        url = f"/api/history/{mac}" if mac else "/api/history/"
        return self._request("GET", url)

    def get_host_by_id(self, host_id: str):
        """
        Get host by ID.
        GET /api/host/{id}
        :param host_id: ID of the host.
        """
        return self._request("GET", f"/api/host/{host_id}")

    def get_port_state(self, addr: str, port: int):
        """
        Get the state of a port.
        GET /api/port/{addr}/{port}
        :param addr: IP address.
        :param port: Port number.
        """
        return self._request("GET", f"/api/port/{addr}/{port}")

    def edit_host(self, host_id: str, name: str, known: str = ""):
        """
        Edit a host's name and optionally toggle its "Known" state.
        GET /api/edit/{id}/{name}/{known}
        :param host_id: ID of the host.
        :param name: New name for the host.
        :param known: Set to 'toggle' to change the known state (optional).
        """
        url = f"/api/edit/{host_id}/{name}/{known}" if known else f"/api/edit/{host_id}/{name}/"
        return self._request("GET", url)

    def delete_host(self, host_id: str):
        """
        Delete a host by ID.
        GET /api/host/del/{id}
        :param host_id: ID of the host to delete.
        """
        return self._request("GET", f"/api/host/del/{host_id}")
