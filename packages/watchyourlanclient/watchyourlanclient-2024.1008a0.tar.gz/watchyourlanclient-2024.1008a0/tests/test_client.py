import pytest
import httpx
from httpx import MockTransport
import asyncio
# Adjust import path based on your project structure
from watchyourlanclient import WatchYourLANClient


@pytest.fixture
def mock_transport():
    """
    Fixture to create a MockTransport for simulating HTTP responses.
    """
    def transport_callback(request: httpx.Request):
        # Simulate different endpoints
        if request.url.path == "/api/all":
            return httpx.Response(200, json=[{"id": "1", "name": "Host1"}, {"id": "2", "name": "Host2"}])
        elif request.url.path.startswith("/api/host/"):
            if request.url.path.startswith("/api/host/del/"):
                # Handle the delete host request
                return httpx.Response(200, json={"result": "deleted"})
            else:
                host_id = request.url.path.split('/')[-1]
                return httpx.Response(200, json={"id": host_id, "name": f"Host{host_id}"})
        elif request.url.path.startswith("/api/history"):
            return httpx.Response(200, json=[{"mac": "00:11:22:33:44:55", "event": "Connected"}])
        elif request.url.path.startswith("/api/port/"):
            return httpx.Response(200, json={"state": "open"})
        elif request.url.path.startswith("/api/edit"):
            return httpx.Response(200, json={"result": "success"})
        return httpx.Response(404)

    return MockTransport(transport_callback)

# Sync Tests


def test_get_all_hosts_sync(mock_transport):
    """
    Test fetching all hosts in synchronous mode.
    """
    api_client = WatchYourLANClient(
        base_url="http://localhost:8840", async_mode=False)
    api_client.client = httpx.Client(
        transport=mock_transport, base_url="http://localhost:8840")

    hosts = api_client.get_all_hosts()
    assert len(hosts) == 2
    assert hosts[0]["name"] == "Host1"
    api_client.close_sync()


def test_get_host_by_id_sync(mock_transport):
    """
    Test fetching a host by ID in synchronous mode.
    """
    api_client = WatchYourLANClient(
        base_url="http://localhost:8840", async_mode=False)
    api_client.client = httpx.Client(
        transport=mock_transport, base_url="http://localhost:8840")

    host = api_client.get_host_by_id("1")
    assert host["id"] == "1"
    assert host["name"] == "Host1"
    api_client.close_sync()


def test_delete_host_sync(mock_transport):
    """
    Test deleting a host in synchronous mode.
    """
    api_client = WatchYourLANClient(
        base_url="http://localhost:8840", async_mode=False)
    api_client.client = httpx.Client(
        transport=mock_transport, base_url="http://localhost:8840")

    response = api_client.delete_host("1")
    assert response["result"] == "deleted"
    api_client.close_sync()

# Async Tests


@pytest.mark.asyncio
async def test_get_all_hosts_async(mock_transport):
    """
    Test fetching all hosts in asynchronous mode.
    """
    api_client = WatchYourLANClient(
        base_url="http://localhost:8840", async_mode=True)
    api_client.client = httpx.AsyncClient(
        transport=mock_transport, base_url="http://localhost:8840")

    hosts = await api_client.get_all_hosts()
    assert len(hosts) == 2
    assert hosts[0]["name"] == "Host1"
    await api_client.close()


@pytest.mark.asyncio
async def test_get_host_by_id_async(mock_transport):
    """
    Test fetching a host by ID in asynchronous mode.
    """
    api_client = WatchYourLANClient(
        base_url="http://localhost:8840", async_mode=True)
    api_client.client = httpx.AsyncClient(
        transport=mock_transport, base_url="http://localhost:8840")

    host = await api_client.get_host_by_id("1")
    assert host["id"] == "1"
    assert host["name"] == "Host1"
    await api_client.close()


@pytest.mark.asyncio
async def test_delete_host_async(mock_transport):
    """
    Test deleting a host in asynchronous mode.
    """
    api_client = WatchYourLANClient(
        base_url="http://localhost:8840", async_mode=True)
    api_client.client = httpx.AsyncClient(
        transport=mock_transport, base_url="http://localhost:8840")

    response = await api_client.delete_host("1")
    assert response["result"] == "deleted"
    await api_client.close()
