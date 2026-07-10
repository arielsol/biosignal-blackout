import asyncio
import msvcrt
import time
import gdx
import global_vars
import handle_osc

if 'gdx_client' not in locals():
    gdx_client = None
    loop = None

def connect():
    global gdx_client, loop
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    gdx_client = gdx.gdx()

    print(f"Searching for device {global_vars.DEVICE_TO_OPEN}...")
    gdx_client.open(connection='ble', device_to_open = global_vars.DEVICE_TO_OPEN) 

    if gdx_client.devices:
        global_vars.device_connected = True
        gdx_client.select_sensors(global_vars.SELECTED_SENSORS)
        global_vars.last_valid_measurements = [0.0] * len(global_vars.SELECTED_SENSORS)
        print("Success! Device connected. Press SPACE to stream sensor data over OSC.")
    else:
        print("Error: No devices found.")
        if loop:
            loop.close()

def handle_stream_input():
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b' ': # Space
            gdx_client.start(period = global_vars.SAMPLE_PERIOD)
            handle_osc.osc_init()
            global_vars.stream_active = True
            print("\nStreaming live data... Press PERIOD to stop streaming.")
            print("-----------------------------------------------------")
        if key == b'.': # Period
            global_vars.stream_active = False
            disconnect()

def disconnect():
    print("\nClosing connections...")

    gdx_client.stop()
    gdx_client.close()
    global_vars.device_connected = False

    loop.close()
    print("Device disconnected.")
    
if __name__ == "__main__":
    connect()

    while global_vars.device_connected:
        handle_stream_input()

        if global_vars.stream_active:
            handle_osc.send_osc(gdx_client)
            
        time.sleep(0.01)

    print("Program exited successfully.")