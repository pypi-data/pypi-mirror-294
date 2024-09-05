# watchyourlanclient
Python API client to interact with WatchYourLAN

# Example usage
```python
from watchyourlanclient import WatchYourLANClient

async def main_async():
    api_client = WatchYourLANClient(base_url="http://localhost:8840", async_mode=True)

    try:
        # Get all hosts
        hosts = await api_client.get_all_hosts()
        print("Async Hosts:", hosts)

        # Get history for a specific MAC
        history = await api_client.get_host_history("00:11:22:33:44:55")
        print("Async Host History:", history)

        # Get port state
        port_state = await api_client.get_port_state("192.168.1.10", 80)
        print("Async Port State:", port_state)

    finally:
        await api_client.close()

def main_sync():
    api_client = WatchYourLANClient(base_url="http://localhost:8840", async_mode=False)

    try:
        # Get all hosts
        hosts = api_client.get_all_hosts()
        print("Sync Hosts:", hosts)

        # Get history for a specific MAC
        history = api_client.get_host_history("00:11:22:33:44:55")
        print("Sync Host History:", history)

        # Get port state
        port_state = api_client.get_port_state("192.168.1.10", 80)
        print("Sync Port State:", port_state)

    finally:
        api_client.close_sync()
```
