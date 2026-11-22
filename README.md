# Biosignal Blackout

An immersive theatre/dance show in which the performers' bodies drive live visuals. Performers wear wireless biosensors: a **Polar Verity Sense** optical heart-rate monitor and a **Vernier Go Direct Respiration Belt**. Small Python bridge scripts read the sensors over Bluetooth LE and stream their values over OSC into a **TouchDesigner** patch. The TD show system renders and plays back the visuals for each act.

```
 Polar Verity Sense ──BLE──▶ PolarVeritySense/hrm_connect.py ──OSC──┐
                                                                     ├──▶ TouchDesigner/Show System.toe ──▶ projection
 Vernier GDX-RB belt ─BLE──▶ VernierGo/belt_connect.py ───────OSC──┘
```

## Requirements

- **Windows.** The bridge scripts read the keyboard through `msvcrt`, which only exists on Windows.
- **Python 3.10+**
- **TouchDesigner** (any build that can open `Show System.toe`)
- A Bluetooth LE adapter, plus the Polar Verity Sense and the Vernier GDX-RB belt, charged and switched on

Install the Python dependencies:

```powershell
pip install python-osc bleak polar-python godirect
```

The `gdx` module is vendored in `VernierGo/gdx/` and needs no install, but you must run `belt_connect.py` from inside `VernierGo/` so Python can find it.

## Configuration

Each bridge reads its settings from a `global_vars.py` file in its own folder. Edit that file to switch between the spare sensors or change the OSC target.

### Polar Verity Sense: `PolarVeritySense/global_vars.py`

| Setting | Default | Notes |
| --- | --- | --- |
| `DEVICE_TO_OPEN` | `'1ABC0538'` | Default will not work: match against the BLE device name. |
| `PPG_CHANNEL_INDEX` | `0` | Optical channel used for the waveform (0–2; channel 3 is ambient light and is subtracted). |
| `OSC_IP_ADDRESS` / `OSC_PORT` | `127.0.0.1` / `3133` | |
| `DEBUG_MODE` | `True` | Prints live values in the terminal. |

### Vernier respiration belt: `VernierGo/global_vars.py`

| Setting | Default | Notes |
| --- | --- | --- |
| `DEVICE_TO_OPEN` | `'GDX-RB 0K7012M6'` | Default will not work: match against the device serial number. |
| `SAMPLE_PERIOD` | `50` | Sampling period in milliseconds (50 ms = 20 samples/sec). |
| `SELECTED_SENSORS` | `[1, 2, 4, 5]` | 1 = Force, 2 = Respiration Rate, 4 = Steps, 5 = Step Rate. |
| `OSC_IP_ADDRESS` / `OSC_PORT` | `127.0.0.1` / `3132` | |
| `DEBUG_MODE` | `True` | Prints live values in the terminal. |

To run TouchDesigner on a different machine from the sensors, set `OSC_IP_ADDRESS` in both files to that machine's IP address.

## OSC messages

All values are rounded to 2 decimals. When a sensor returns NaN, the last valid value is sent again, so TouchDesigner never receives NaN.

| Address | Value |
| --- | --- |
| `/hrm/value0` | Heart rate (BPM) |
| `/hrm/value1` | PPG waveform (raw optical signal minus ambient light) |
| `/belt/sensor0` | Force (breathing pressure on the belt) |
| `/belt/sensor1` | Respiration rate |
| `/belt/sensor2` | Steps |
| `/belt/sensor3` | Step rate |

The belt addresses follow the order of `SELECTED_SENSORS`. If you change that list, the meaning of `/belt/sensorN` changes with it.

## Running the show

Either order works. Starting TouchDesigner first is preferred.

1. **Open TouchDesigner**: load `TouchDesigner/Show System.toe`.
2. **Start the heart-rate bridge** in its own terminal:
   ```powershell
   cd PolarVeritySense
   ```
   ```powershell
   python hrm_connect.py
   ```
   Wait for `Success! Polar device connected.`
3. **Start the belt bridge** in a second terminal:
   ```powershell
   cd VernierGo
   ```
   ```powershell
   python belt_connect.py
   ```
   Wait for `Success! Device connected.`
4. When the performers are ready, **press `SPACE`** in each bridge terminal to start streaming. With `DEBUG_MODE` on, live values appear on a single updating line.
5. After the show, **press `.` (period)** in each terminal to stop streaming and disconnect the sensor cleanly. `Ctrl+C` also works for the heart-rate bridge.

Keyboard input only works while that terminal window has focus.

## Troubleshooting

- **`Heartbeat device not found` / `No devices found`**: make sure the sensor is on, charged, and not paired to another app or computer (Polar Flow, Vernier Graphical Analysis). Check that `DEVICE_TO_OPEN` matches the unit you are holding. The Polar scan gives up after 5 seconds; run the script again to retry.
- **No data in TouchDesigner**: check that the OSC In CHOP/DAT ports in the show file match 3132/3133, and that no other program is already using those ports. Also check that Windows Firewall isn't blocking Python when TouchDesigner runs on another machine.
- **`ModuleNotFoundError: gdx`**: run `belt_connect.py` from inside the `VernierGo/` folder.
- **`ModuleNotFoundError: msvcrt`**: the scripts are Windows-only.

## License

Apache License 2.0. See [LICENSE](LICENSE). The vendored `VernierGo/gdx/` module comes from Vernier Software & Technology's [godirect-examples](https://github.com/VernierST/godirect-examples).
