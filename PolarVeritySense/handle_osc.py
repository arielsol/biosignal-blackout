import math
import global_vars
from pythonosc import udp_client

osc_client = None
    
def osc_init():
    global osc_client
    osc_client = udp_client.SimpleUDPClient(global_vars.OSC_IP_ADDRESS, global_vars.OSC_PORT)
    print(f"OSC Client initialized. \n \nIP Address: {global_vars.OSC_IP_ADDRESS} \nPort: {global_vars.OSC_PORT}")

def send_osc(measurements):
    global osc_client 

    if osc_client is None:
        osc_init()
    
    if measurements:
        for idx, val in enumerate(measurements):
            if not math.isnan(val):
                global_vars.last_valid_measurements[idx] = val
            else:
                val = global_vars.last_valid_measurements[idx]
        
            osc_client.send_message(f"/armband/value{idx}", round(val, 2))

        if global_vars.DEBUG_MODE:
            debug_sensor_data(global_vars.last_valid_measurements)

def debug_sensor_data(measurements):
    LABELS = ["Heart Rate", "PPG Waveform"]
    
    debug_segments = []

    for idx, val in enumerate(measurements):
        # Fallback case if index has no label
        label = LABELS[idx] if idx < len(LABELS) else f"Sensor {idx}"
        
        if val == int(val):
            formatted_val = f"{int(val)}"
            if label == "Heart Rate":
                formatted_val += " BPM"
        else:
            formatted_val = f"{val:.2f}"
            
        debug_segments.append(f"{label}: {formatted_val}")

    full_line = " | ".join(debug_segments)
    print(f"{full_line}" + " " * 20, end="\r", flush=True)