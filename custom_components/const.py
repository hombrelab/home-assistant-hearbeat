#  Copyright (c) 2021 Hombrelab <me@hombrelab.com>

import voluptuous as vol

DOMAIN = 'heartbeat'
UUID = '1b37546a-909d-476b-bd69-e1775e6c1aa7'

SW_MANUFACTURER = 'Hombrelab'
SW_NAME = 'Heartbeat'
SW_MODEL = 'mqtt'
SW_VERSION = "1.0.000"

# labels
ENTITY_NAME = 'name'
TOPIC_NAME = 'topic'

# default values
NAME_VALUE = 'heartbeat'
TOPIC_VALUE = 'home-assistant/{app}/heartbeat'

# list of entities
ENTITIES = [
    [
        'Heartbeat status',
        'mdi:heart',
        None,
        'status'
    ],
    [
        'Heartbeat application',
        'mdi:application',
        None,
        'app_name'
    ],
    [
        'Heartbeat interval',
        'mdi:timer-outline',
        None,
        'interval'
    ],
    [
        'Heartbeat datetime',
        'mdi:history',
        None,
        'date_time'
    ],
    [
        'Heartbeat timestamp',
        'mdi:history',
        None,
        'timestamp'
    ]
]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                    vol.Required(ENTITY_NAME, default=NAME_VALUE): str,
                    vol.Required(TOPIC_NAME, default=TOPIC_VALUE): str,
            }
        )
    },
    extra=vol.ALLOW_EXTRA
)
