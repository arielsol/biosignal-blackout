# Name of device to connnect
DEVICE_TO_OPEN = '1ABC0538'

# Optical sensor channels available:
    # 0: Primary signal channel
    # 1: Secondary signal channel
    # 2: Tertiary signal channel
    # 3: Ambient light baseline (do not use)
PPG_CHANNEL_INDEX = 0

# OSC settings
OSC_IP_ADDRESS = "127.0.0.1"
OSC_PORT = 3133

# Print sensor data in terminal
DEBUG_MODE = True

device_connected = False

stream_active = False

last_valid_measurements = [0, 0.0]