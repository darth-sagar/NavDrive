---

## NAVDRIVE - STAGE 3: IMPLEMENTATION

📍 OVERVIEW
This phase involves deploying the trained TFLite model on the Raspberry Pi and running real-time inference based on live camera input. The predicted steering values are then sent to the Arduino over serial communication to control the movement of the car.

---

1. MODEL DEPLOYMENT ON RASPBERRY PI

---

Steps:

1. Copy the trained TFLite model from PC to Raspberry Pi:

2. Place the following scripts on the Pi:
   - `main.py` — handles camera input, model inference, and serial transmission
3. Make a virtual environment and activate it:

```bash
raspberrypi@raspberrypi:~ $ python3 -m venv myenv
raspberrypi@raspberrypi:~ $ source myenv/bin/activate
```
4. Install required Python dependencies:

```bash
pip install -r requirements.txt
```

For Dependencies follow the `requirement.txt` in the `docs` :


---

2. REAL-TIME CAMERA INFERENCE

---

Once the setup is ready:

1. Attach the Pi Camera to the CSI port
2. Run the script:
3. Activate the virtual environment if not already done:

```bash
python3 main.py
```

This will:

- Continuously capture images from the Pi Camera
- Preprocess them for model input
- Run inference using the loaded `model.tflite`
- Output a steering angle prediction per frame
- A small window will open that shows the real time camera feed
- Overlay predicted values on the screen

Note :

- Enable the ssh connection and enable realvnc connection as well
- Login in to Realvnc Desktop version place the address of the raspberry pi in the address bar it should connect
- you will be able to see the predicted Values on the Desktop Screen

it should look like this :
![](/stage_3_Implementation/Docs/assets/sample.png)

---

3. SERIAL COMMUNICATION WITH ARDUINO

---

The predicted value is transmitted from Raspberry Pi to Arduino via USB (serial communication).

🛠️ Setup:

- Arduino listens on Serial at baud rate: **115200**
- Raspberry Pi sends steering values using:

```python
serial.write(f"{angle}\n".encode())
```

✔️ Ensure:

- The Arduino is connected via USB (e.g., `/dev/ttyUSB0`)
- Arduino sketch is uploaded and listening via:

```cpp
Serial.begin(115200);
```

---

4. ARDUINO CONTROL LOGIC

---

On the Arduino:

- Read incoming serial values
- Map the steering angle to motor control signals (e.g., PWM, direction)
- Move the motors accordingly to turn or go straight

📁 Example File:

- `navdrive_manual_mode.ino` can be adapted to include `Serial.read()` and control motors

---

5. FINAL NOTES

---

✅ Make sure both Raspberry Pi and Arduino are powered correctly
✅ Use error handling for serial disconnects or model errors
✅ Test in a safe area before running on full-speed tracks
✅ Consider adding a kill switch or emergency stop
