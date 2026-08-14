# Name of device to connnect - available:
    #GDX-RB 0K7012M6
    #GDX-RB 0K701450
DEVICE_TO_OPEN = 'GDX-RB 0K7012M6'

# Collects data at this rate, milliseconds (500ms = 2 samples/sec)
SAMPLE_PERIOD = 50 

# [1] Force
# [2] Respiratory Rate
# [4] Steps
# [5] Step Rate
SELECTED_SENSORS = [1, 2, 4, 5]

# Print sensor data in terminal
DEBUG_MODE = True

# OSC settings
OSC_IP_ADDRESS = "127.0.0.1"
OSC_PORT = 3132

device_connected = False

stream_active = False

last_valid_measurements = []