# Home Assistant Ambient Desktop
Dynamically set your Home Assistant lights to match the colour of your screen

## Motivation

This project was inspired by [AmbientLightToHA](https://github.com/LeonBurghardtDev/AmbientLightToHA) which is exactly what I want, however my computer runs Wayland+Gnome which doesn't support [`wlr-screencopy-unstable-v1` used by grim](https://github.com/emersion/grim/issues/58#issuecomment-512764541).

My approach is to instead use OBS Studio to capture my screen as a virtual camera. I can then pull frames from that device, analyse the colours and send it on to Home Assistant. Using OBS also makes this fairly platform-agnostic unlike an implementation with a Wayland-specific backend.

This project also serves as a learning exercise for using NumPy and performing minor image processing.

# Usage
## Setup
1. Create a "Long-lived access token" in Home Assistant (User profile -> Security -> Long-lived access tokens -> Create token)
2. Create a `.env` file using the contents of `.env.example` as a template
3. Install the requirements: `python3 -m pip install -r requirements.txt`
4. Create an automation in Home Assistant using the `light.turn_on` tied to the value of the sensor entity (`sensor.ambient_light` by default).


<details>
<summary>Example Home Assistant Automation</summary>

```yaml
triggers:
  - trigger: state
    entity_id: sensor.ambient_light
actions:
  - action: light.turn_on
    target:
      entity_id: light.my_light
    data:
      rgb_color: |
        {{ [
          state_attr('sensor.ambient_light', 'r'),
          state_attr('sensor.ambient_light', 'g'),
          state_attr('sensor.ambient_light', 'b')
        ] }}
      transition: 0.5
```

</details>

## Running
1. Launch OBS, add your desktop as a video source, and start the virtual camera
2. Run the script with `python3 main.py`


# Credits
- Heavy inspiration taken from https://github.com/LeonBurghardtDev/AmbientLightToHA
- Colour extraction algorithm is from https://modern-colorthief.readthedocs.io/en/stable/mmcq.html