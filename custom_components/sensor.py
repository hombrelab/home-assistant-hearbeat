#  Copyright (c) 2021 Hombrelab <me@hombrelab.com>

import json
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.restore_state import RestoreEntity
from typing import Any, Dict

from . import HeartbeatDevice
from .const import (
    DOMAIN,
    UUID,

    ENTITIES,

    ENTITY_NAME,
    TOPIC_NAME,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry, async_add_entities):
    """set up entities based on a config entry"""

    entities = [
        HeartbeatEntity(
            entry.data[ENTITY_NAME], name, icon, unit, element
        )
        for name, icon, unit, element in ENTITIES
    ]

    async_add_entities(entities)

    async def async_hearbeat_callback(message):
        """handle calls to the service."""
        if message is not None:
           payload = message.payload
           heartbeat = json.loads(payload)

        _LOGGER.debug(payload)

        for entity in entities:
            entity.set_heartbeat(heartbeat)

            #hass.async_create_task(entity.async_update_ha_state())

    mqtt = hass.components.mqtt

    hass.async_create_task(
        mqtt.async_subscribe(
            entry.data[TOPIC_NAME],
            async_hearbeat_callback,
            0,
        ),
    )


class HeartbeatEntity(HeartbeatDevice, RestoreEntity):
    """representation of an entity"""

    def __init__(self, device, name, icon, unit, element):
        """initialize the entity"""
        super().__init__(device)

        self._device = device.lower().replace(" ", "_")
        self._name = f"{device} {name}"
        self._icon = icon
        self._unit = unit
        self._element = element

        self._state = '-'
        self._attributes = {}

    async def async_added_to_hass(self):
        """run when entity is about to be added"""
        await super().async_added_to_hass()

        state = await self.async_get_last_state()

        if state:
            try:
                self._state = state.state
                self._attributes = state.attributes
            except Exception as err:
                _LOGGER.warning(f"could not restore {self._element}: {err}")

    def set_heartbeat(self, data):
        """set the heartbeat for heartbeat"""
        if data is not None:
            self._state = data.get(self._element)

    @property
    def unique_id(self):
        """return the unique id"""
        return f'{UUID}.{self._device}.{self._element}'

    @property
    def name(self):
        """return the name of the entity"""
        return self._name

    @property
    def icon(self):
        """return the icon to be used for this entity"""
        return self._icon

    @property
    def unit_of_measurement(self):
        """return the unit of measurement"""
        return self._unit

    @property
    def state(self):
        """return the state of the entity"""
        return self._state

    @property
    def device_state_attributes(self):
        """return the state attributes"""
        return self._attributes
