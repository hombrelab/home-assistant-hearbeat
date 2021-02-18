#  Copyright (c) 2021 Hombrelab <me@hombrelab.com>

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from .const import (
    DOMAIN,
    UUID,

    SW_MANUFACTURER,
    SW_NAME,
    SW_MODEL,
    SW_VERSION,
)

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistantType, config: ConfigEntry):
    """set up component"""
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        return True

    hass.data[DOMAIN] = config

    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """load config entries"""
    hass.data[DOMAIN][entry.entry_id] = UUID

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """unload config entries"""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class HeartbeatDevice():
    def __init__(self, device):
        self._device = device

    @property
    def device_info(self):
        """return device information"""
        return {
            "identifiers": {
                (DOMAIN,
                 UUID,
                 self._device)
            },
            "name": SW_NAME,
            "manufacturer": SW_MANUFACTURER,
            "model": SW_MODEL,
            "sw_version": SW_VERSION,
        }
