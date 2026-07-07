
'''
# SIGNAL VARIANCE SCRIPT
import numpy as np

def ppg_callback(data: PPGData):
    if len(data.samples) < 5:
        return

    # 1. Extract the full array of values for each channel from the packet
    # (Subtracting ambient light from each channel)
    ch0 = [s.ppg[0] - s.ppg[3] for s in data.samples]
    ch1 = [s.ppg[1] - s.ppg[3] for s in data.samples]
    ch2 = [s.ppg[2] - s.ppg[3] for s in data.samples]

    # 2. Calculate the standard deviation (amplitude variance) of the packet
    std_ch0 = np.std(ch0)
    std_ch1 = np.std(ch1)
    std_ch2 = np.std(ch2)

    # 3. Define what a "dead" or "wildly noisy" signal looks like
    # (You would tune these thresholds by printing values during testing)
    MIN_VAL = 500      # Flatline threshold
    MAX_VAL = 50000    # Extreme motion/noise threshold

    # 4. Route the best channel's last sample to your global variable
    if MIN_VAL < std_ch0 < MAX_VAL:
        best_sample = ch0[-1]
    elif MIN_VAL < std_ch1 < MAX_VAL:
        best_sample = ch1[-1]  # Fallback 1
    elif MIN_VAL < std_ch2 < MAX_VAL:
        best_sample = ch2[-1]  # Fallback 2
    else:
        best_sample = global_vars.last_valid_measurements[1] # Keep old value if all are noisy

    global_vars.last_valid_measurements[1] = float(best_sample)
'''

'''
async def async_start_stream():
    print("Initializing streams on Verity Sense...")

    def hr_callback(data: HRData):
        bpm_value = getattr(data, 'bpm', getattr(data, 'heart_rate', 0))
        global_vars.last_valid_measurements[0] = bpm_value

    def ppg_callback(data: PPGData):
        samples_list = getattr(data, 'samples', getattr(data, 'ppg_data', None))
        
        if samples_list:
            latest_sample = samples_list[-1]
            
            # Subtract ambient noise directly by using list indices
            raw_signal = latest_sample[global_vars.PPG_CHANNEL_INDEX] 
            ambient_light = latest_sample[3]
            waveform_value = float(raw_signal - ambient_light)
            
            global_vars.last_valid_measurements[1] = waveform_value

    await polar_device.start_hr_stream(hr_callback=hr_callback)
    await polar_device.start_ppg_stream(ppg_callback=ppg_callback, sample_rate=55, resolution=22, channels=4)
    print("Streams successfully initialized.")
'''