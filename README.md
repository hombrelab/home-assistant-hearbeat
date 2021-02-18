# Heartbeat
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/hombrelab/home-assistant-heartbeat) ![GitHub commit activity](https://img.shields.io/github/last-commit/hombrelab/home-assistant-heartbeat)  

The [Heartbeat](https://github.com/hombrelab/home-assistant-heartbeat) custom component for [home-assistant](https://www.home-assistant.io) is created to capture a heartbeat from custom application I have running.


### Installation
Copy this folder to `<config_dir>/custom_components/heartbeat/` or use [hacs](https://github.com/custom-components/hacs) and point it to this [GitHub repository](https://github.com/hombrelab/home-assistant-heartbeat).  

Setup is done through the integration page:  
- **name**: _required_ (you can have more than one setup so choose a unique name)  
- topic: _required_ the mqtt topic to subscribe to  

A json is received with:

```json
{
    "appName": "",
    "status": "online/offline",
    "interval":  0,
    "date_time":  "",
    "timestamp": 0
}
```

I then setup a template like this:

```yaml
# Watermeter Heartbeat
- platform: template
  sensors:
    watermeter_heartbeat:
      friendly_name: "Watermeter Heartbeat"
      unique_id: watermeter.heartbeat
      icon_template: >-
        {%- if is_state("sensor.watermeter_heartbeat_status", "online") %}
          mdi:heart
        {%- elif is_state("sensor.watermeter_heartbeat_status", "offline") %}
          mdi:heart-off
        {%- else %}
          mdi:heart-broken
        {%- endif %}
      value_template: >-
        {%- if states('sensor.watermeter_heartbeat_timestamp') -%}
          {% set timestamp = states('sensor.watermeter_heartbeat_timestamp') | int | timestamp_custom('%H:%M:%S', true) %}
          {{timestamp}}
        {%- else -%}
          -
        {%- endif -%}
      availability_template: >-
        {%- if is_state("sensor.watermeter_heartbeat_status", "online") %}
          true
        {%- endif %}
```