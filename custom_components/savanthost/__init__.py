import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_HOST, CONF_PORT, SCAN_INTERVAL_SECONDS
from .api import SavantClient
from .discovery import SavantDiscovery

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["scene"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the SavantHost component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up SavantHost from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    
    session = async_get_clientsession(hass)
    client = SavantClient(session, host, port)

    async def async_update_data():
        """Fetch data from API."""
        try:
            scenes = await client.get_scenes()
        except Exception:
            _LOGGER.warning("Connection lost, attempting to re-discover Savant Host...")
            # Try to discover
            discovery = SavantDiscovery(hass)
            hosts = await discovery.discover()
            
            if hosts:
                # Use the first found host
                new_host = hosts[0]
                new_ip = new_host["ip"]
                new_port = new_host["port"]
                
                _LOGGER.info(f"Re-discovered host at {new_ip}:{new_port}")
                
                # Update client
                client.host = new_ip
                client.port = new_port
                client.base_url = f"http://{new_ip}:{new_port}"
                
                # Update ConfigEntry
                hass.config_entries.async_update_entry(
                    entry,
                    data={**entry.data, CONF_HOST: new_ip, CONF_PORT: new_port}
                )
                
                # Retry fetch
                try:
                    scenes = await client.get_scenes()
                except Exception as e:
                    raise UpdateFailed(f"Error communicating with API after re-discovery: {e}")
            else:
                raise UpdateFailed("Connection lost and re-discovery failed")

        if scenes is None:
            # Don't raise UpdateFailed for empty scenes/error status, just return empty
            _LOGGER.debug("No scenes found or API error")
            return []
        return scenes

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="savant_scenes",
        update_method=async_update_data,
        update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "client": client
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
