import math
import global_vars
from pythonosc import udp_client

osc_client = None
    
def osc_init():
    global osc_client
    osc_client = udp_client.SimpleUDPClient(global_vars.OSC_IP_ADDRESS, global_vars.OSC_PORT)
    print(f"OSC Client initialized. \n \nIP Address: {global_vars.OSC_IP_ADDRESS} \nPort: {global_vars.OSC_PORT}")

def send_osc(gdx_client):
    global osc_client 

    if osc_client is None:
        osc_init()
    
    measurements = gdx_client.read() 
    if measurements:
        
        # Don't pass NaN
        for idx, val in enumerate(measurements):
            if not math.isnan(val):
                global_vars.last_valid_measurements[idx] = val
            else:
                val = global_vars.last_valid_measurements[idx]
        
            osc_client.send_message(f"/belt/sensor{idx}", round(val, 2))

        if global_vars.DEBUG_MODE:
            debug_sensor_data(global_vars.last_valid_measurements)

def debug_sensor_data(measurements):
    # If measurements is empty or None, get out early to prevent errors
    if not measurements:
        return

    debug_segments = []

    # Iterate through your selected sensors using their relative index in the list
    for idx, sensor_id in enumerate(global_vars.SELECTED_SENSORS):
        # Ensure we don't accidentally look for an index that doesn't exist in the data chunk
        if idx >= len(measurements):
            break
            
        val = measurements[idx]

        # Build clean string labels based on the active sensor ID
        if sensor_id == 1:
            debug_segments.append(f"Force: {val:.2f}")
        elif sensor_id == 2:
            debug_segments.append(f"Resp Rate: {val:.2f}")
        elif sensor_id == 4:
            debug_segments.append(f"Steps: {val:.2f}")
        elif sensor_id == 5:
            debug_segments.append(f"Step Rate: {val:.2f}")

    # Join all active segments together with a clean spacer divider
    # Example output: "Force: 14.20 | Resp Rate: 12.00 | Steps: 420.00"
    full_line = " | ".join(debug_segments)

    # Print the unified line, add trailing spaces to erase old data artifacts, and return to start
    print(f"{full_line}", end="                                        \r", flush=True)