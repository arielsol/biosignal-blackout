import asyncio
import msvcrt
import global_vars
import handle_osc

from bleak import BleakScanner
from polar_python import PolarDevice
from polar_python.models import PPGData, HRData 

polar_device = None
loop = None

async def async_connect():
    global polar_device
    print(f"Searching for device containing '{global_vars.DEVICE_TO_OPEN}'...")
    
    device = await BleakScanner.find_device_by_filter(
        lambda bd, ad: bd.name and global_vars.DEVICE_TO_OPEN in bd.name, timeout=5
    )
    
    if not device:
        print("Error: Heartbeat device not found.")
        return False

    print(f"Found {device.name}, establishing connection...")
    polar_device = PolarDevice(device)
    
    await polar_device.connect()
    return True

async def async_start_stream():
    print("Initializing streams on Verity Sense...")

    def hr_callback(data: HRData):
        global_vars.last_valid_measurements[0] = data.heartrate

    def ppg_callback(data: PPGData):
        if data.samples:
            latest_sample = data.samples[-1]
            
            raw_signal = latest_sample[global_vars.PPG_CHANNEL_INDEX] 
            ambient_light = latest_sample[3] 
            waveform_value = float(raw_signal - ambient_light)

            global_vars.last_valid_measurements[1] = waveform_value

    await polar_device.start_hr_stream(hr_callback=hr_callback)
    await polar_device.start_ppg_stream(
        ppg_callback=ppg_callback, 
        sample_rate=55, 
        resolution=22, 
        channels=4
    )
    print("Streams successfully initialized.")

async def async_disconnect():
    global polar_device
    if polar_device:
        try:
            await polar_device.disconnect()
        except Exception as e:
            print(f"Error cleanly disconnecting: {e}")

# --- Asynchronous Main Loop & Execution Wrapper ---

def connect():
    global loop
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    success = loop.run_until_complete(async_connect())

    if success:
        global_vars.device_connected = True
        print("Success! Polar device connected. Press SPACE to stream sensor data over OSC.")
        try:
            loop.run_until_complete(async_main_loop())
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
        finally:
            if not loop.is_closed():
                disconnect()
    else:
        global_vars.device_connected = False
        loop.close()

async def async_main_loop():
    last_sent_data = list(global_vars.last_valid_measurements)

    while global_vars.device_connected:
        handle_stream_input()

        if global_vars.stream_active:
            current_data = global_vars.last_valid_measurements
            
            if current_data != last_sent_data:
                handle_osc.send_osc(current_data)
                last_sent_data = list(current_data)
            
        await asyncio.sleep(0.01)

def handle_stream_input():
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b' ': # Space
            loop.create_task(async_start_stream())
            handle_osc.osc_init()
            global_vars.stream_active = True
            print("\nStreaming live data... Press PERIOD to stop streaming.")
            print("-----------------------------------------------------")
        if key == b'.': # Period
            global_vars.stream_active = False
            global_vars.device_connected = False

def disconnect():
    global loop
    print("\nClosing connections...")

    if loop and not loop.is_closed():
        loop.run_until_complete(async_disconnect())
        loop.close()

    print("Device disconnected.")
    
if __name__ == "__main__":
    connect()
    print("Program exited successfully.")