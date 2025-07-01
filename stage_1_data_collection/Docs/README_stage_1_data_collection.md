
===============================================
NAVDRIVE - STAGE 1: DATA COLLECTION
===============================================

📍 OVERVIEW:
This phase focuses on preparing the hardware setup and collecting data from manual driving. The collected data will later be used to train a steering prediction model.

-----------------------------------------------
1. HARDWARE COLLECTION / PREPARATION
-----------------------------------------------

Gather the following components before beginning:

🔌 Required Components:
- Raspberry Pi 3B
- Pi Camera Module
- Arduino Uno / Nano
- CT6B Transmitter + Receiver
- 2 x Ultrasonic Sensors (Front & Rear)
- MPU6050 (IMU Sensor)
- Motor Driver (L293D or compatible shield)
- DC Gear Motors with wheels
- Chassis/Base
- 11.1V 3S LiPo Battery (Motor Power)
- Power bank (Raspberry Pi)
- Jumper Wires, Breadboard or PCB
- USB cable (Arduino to Pi)

Optional:
- Custom acrylic/wooden body for neat wiring

Ensure all components are tested individually before moving to full integration.

-----------------------------------------------
2. CIRCUIT CONNECTION & ASSEMBLY
-----------------------------------------------

Follow the diagrams provided in:

📁 `diagram/`

- `wiring_diagram.png`: Full schematic of all hardware connections
- `pin_mapping.png`: Shows which pins connect to what (on both Arduino and Pi)

Basic connections include:
- Pi Camera → Raspberry Pi CSI port
- Ultrasonic sensors → Arduino digital pins (Trig & Echo)
- MPU6050 → Arduino I2C (SDA, SCL)
- CT6B Receiver → Arduino PWM input pins
- Motor Driver → Arduino + Motors
- Arduino → Raspberry Pi (via USB Serial or UART)

Secure all components on your chassis to avoid disconnection during movement.

-----------------------------------------------
3. CUSTOM TRACK SETUP FOR DATA COLLECTION
-----------------------------------------------

🏗️ Build a custom track either indoors or outdoors:

Indoor Ideas:
- Use black tape on a white floor or cardboard to create paths
- Include curves, straight lines, and intersections

Outdoor Ideas:
- Use chalk, cones, ropes, or tape on smooth cement/tile surface

Make sure:
- The track simulates real-world driving conditions
- There's enough space to make wide turns

-----------------------------------------------
4. DATA COLLECTION PROCESS
-----------------------------------------------

🚘 Drive the car manually using the CT6B transmitter.

📸 Raspberry Pi captures real-time camera frames
📟 Arduino reads CT6B PWM signals (steering input), ultrasonic distance, and IMU data

📁 Data saved:
- Images → `/dataset/raw_images/`
- Sensor data + labels → `/dataset/data.csv`

Each row in `data.csv` will include:
timestamp, image_path, steering_angle, front_distance, rear_distance, imu_x, imu_y, imu_z

-----------------------------------------------
5. OUTPUT EXAMPLE
-----------------------------------------------

``After one successful session:
stage_1_data_collection/
├── dataset/
│   ├── raw_images/
│   │   ├── 20250701_123455.jpg
│   │   └── ...
│   └── data.csv
├── arduino/
│   └── data_collector.ino
├── raspberry_pi/
│   ├── collect_data.py
│   └── ...
├── diagram/
│   ├── wiring_diagram.png
│   └── pin_mapping.png
└── README.txt``

-----------------------------------------------
6. TIPS FOR HIGH-QUALITY DATA
-----------------------------------------------

✅ Vary lighting conditions (dim, bright)
✅ Drive at different speeds and styles
✅ Collect at least 5000–10,000 frames
✅ Avoid sudden jerks while driving
✅ Label or remove corrupt/blank frames

-----------------------------------------------
End of README — Phase 1: Data Collection
===============================================
