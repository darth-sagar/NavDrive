-----------------------------------------
NAVDRIVE - STAGE 1: DATA COLLECTION
-----------------------------------------

📍 OVERVIEW:
This phase focuses on preparing the hardware setup and collecting data from manual driving. The collected data will later be used to train a steering prediction model.

-----------------------------------------------
1. HARDWARE COLLECTION / PREPARATION
-----------------------------------------------

Gather the following components before beginning:

🔌 Required Components:
- Raspberry Pi 3B(or better model or just get a jetson nano)
- Pi Camera Module
- Arduino Uno
- Arduino Uno Shield V5 Expansion Board
- Servo Motor SG90
- CT6B Transmitter + Receiver
- Motor Driver (L293D or compatible shield)
- DC Gear Motors with wheels
- Chassis/Base
- 11.1V 3S LiPo Battery (Motor Power)
- LM2596S DC-DC Buck Converter Module
- XL4015E1 DC-DC Buck Converter Module
- Jumper Wires, Breadboard or PCB
- USB cable (Arduino to Pi)

Optional:
- Custom acrylic/wooden body for neat wiring

Ensure all components are tested individually before moving to full integration.

-----------------------------------------------
2. CIRCUIT CONNECTION & ASSEMBLY
-----------------------------------------------

Follow the diagrams provided in:

📁 `Diagram/`

Full schematic of all hardware connections and Shows which pins connect to what (on both Arduino and Pi)
here they are 
![](/stage_1_data_collection/Docs/Diagram/Ardiuno.png)
![](/stage_1_data_collection/Docs/Diagram/Raspberry_pi.png)

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
- The Track should be 2 times wide the original car chasis or less 

-----------------------------------------------
4. DATA COLLECTION PROCESS
-----------------------------------------------

🚘 Drive the car manually using the CT6B transmitter.

📸 Raspberry Pi captures real-time camera frames
📟 Arduino reads CT6B PWM signals (steering input), ultrasonic distance, and IMU data

📁 Data saved:
- Images → `/dataset/images/`
- Sensor data + labels → `/dataset/data.csv`

Each row in `data.csv` will include:
timestamp, image_path, steering_angle, 

-----------------------------------------------
5. OUTPUT EXAMPLE
-----------------------------------------------

```After one successful session:
data_runs/
├── run-0001/
│   ├── images/
│   │   ├── 20250701_123455.jpg
│   │   └── ...
│   └── data.csv
├── run-0002/
│   ├── images/
│   │   ├── 20250701_123455.jpg
│   │   └── ...
│   └── data.csv
.
.
.
├── raspberry_pi/
│   ├── collect_data.py
│   └── ...
└── README.txt
```

-----------------------------------------------
6. TIPS FOR HIGH-QUALITY DATA
-----------------------------------------------

✅ Vary lighting conditions (dim, bright)
✅ Drive at different speeds and styles
✅ Collect at least 5000–10,000 Images(i Took almost 30,000)
✅ Avoid sudden jerks while driving
✅ Label or remove corrupt/blank frames


