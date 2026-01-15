import logging
import asyncio
from typing import List, Dict, Optional
from homeassistant.core import HomeAssistant
from homeassistant.components import zeroconf as ha_zeroconf
from zeroconf import ServiceBrowser, ServiceStateChange

_LOGGER = logging.getLogger(__name__)

class SavantDiscovery:
    """Helper to discover Savant hosts using Zeroconf."""

    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.found_hosts: List[Dict] = []
        self._browser = None

    def _process_service_info(self, info) -> None:
        """Process discovered service info."""
        if not info.addresses:
            return

        # Prefer IPv4
        ip = None
        for addr in info.addresses:
            # simple check for IPv4 (4 bytes)
            if len(addr) == 4:
                ip = ".".join(map(str, addr))
                break
        
        if not ip:
            return

        host_entry = {
            "ip": ip,
            "port": info.port,
            "name": info.name,
            "hostname": info.server,
        }
        
        # Check if already exists
        if not any(h["ip"] == ip for h in self.found_hosts):
            _LOGGER.info(f"Discovered Savant Host: {host_entry}")
            self.found_hosts.append(host_entry)

    async def discover(self, timeout: int = 5) -> List[Dict]:
        """Run discovery for a specified timeout."""
        self.found_hosts = []
        # Try both with and without .local. suffix, and just _tcp
        service_types = [
            "_soapi_sdo._tcp.local.",
        ]
        
        try:
            # Get shared zeroconf instance
            zc = await ha_zeroconf.async_get_instance(self.hass)
            
            def on_service_state_change(zeroconf_obj, service_type, name, state_change):
                _LOGGER.debug(f"Service state change: {name} {state_change}")
                if state_change is ServiceStateChange.Added:
                    info = zeroconf_obj.get_service_info(service_type, name)
                    if info:
                        _LOGGER.debug(f"Found service info: {info}")
                        self._process_service_info(info)

            self._browser = ServiceBrowser(
                zc, service_types, handlers=[on_service_state_change]
            )

            # Wait for discovery
            await asyncio.sleep(timeout)
            
            # We should strictly NOT close the shared zeroconf instance
            self._browser.cancel()
        except Exception as e:
            _LOGGER.error(f"Error during discovery: {e}")
            
        return self.found_hosts
