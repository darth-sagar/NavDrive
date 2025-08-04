# 🚗 NavDrive - Autonomous Car Project

NavDrive is a real-time autonomous car driving system built using Raspberry Pi, Arduino, and Deep Learning. It captures driving data, trains a CNN to predict steering angles from camera images, and deploys the model for autonomous driving on custom tracks.

---

## 📁 Project Stages

The project is divided into three main stages:

### 🔹 Stage 1: Data Collection

- Assemble the hardware (Raspberry Pi, Arduino, Pi Camera, etc.)
- Manually drive using a CT6B transmitter
- Collect image and sensor data
- Save to `data_runs/`

### 🔹 Stage 2: Model Development

- Transfer data to PC
- Clean and preprocess data
- Train a CNN model to predict steering angle
- Export the trained model as TFLite
- Details in `stage_2_model_training/`

### 🔹 Stage 3: Implementation

- Deploy TFLite model to Raspberry Pi
- Run real-time inference using camera feed
- Send steering prediction to Arduino via Serial
- Arduino drives motors accordingly
- Found in `stage_3_implementation/`

---

## 📷 Real Project Images

Project build photos can be found in:

```
/assets/
├── hardware_setup.jpg
├── indoor_track.jpg
├── loss_curve.png
├── sample_prediction.png
```

![Setup](/assets/2025-03-23-22-09-45-179.jpg)
![Setup](/assets/2025-03-23-22-12-22-518.jpg)
![Track](/assets/Tracks-%20(2).jpg)
![Track](/assets/Tracks-%20(3).jpg)
![Track](/assets/Tracks-%20(4).jpg)
![Track](/assets/Tracks-%20(1).jpg)

---

## 📑 Documentation

Check full project PPT and design docs here:

📁 [`/docs/`](./Docs/)

---

## 🛠️ Requirements

- Raspberry Pi 3B(or later version and jetson nano is preferred)
- Pi Camera
- Arduino Uno/Nano
- CT6B Transmitter and Receiver
- Motor Driver + Motors
- Python 3, OpenCV, TensorFlow Lite, pySerial

---

## 🔗 Useful YouTube Links 

- [Raspberry Pi Controlled RC Car](https://youtube.com/playlist?list=PLBOR4EkbOQUcWIBeEX18JCNEuI2duvipk&si=3MRvOiMpJ9jW0Hu2)
- [OpenCV Neural Network Self driving Car using Neural Network](https://youtube.com/playlist?list=PLMoSUbG1Q_r9h_imTd2xYCT5udwDMU-sa&si=sHZwSKlA2JtqpozQ)
- [Self Driving Robot Car with traffic Sign Detection| Using OpenCV, Raspberry pi and ESP32](https://youtu.be/TRhhV0wUqsY?si=W5YdkAo1iAmRCspn)
- [Self Driving car using Raspberry Pi and Open CV | Lane Detection | Autonomous Driving](https://youtu.be/KnkEJL3IH1Q?si=6BlFHcheMwUkQ018)

---

## 📬 Contact

👤 **Sagar Saini**  
📧 Email: [sagarsaini9531@gmail.com]  

---

## ✅ To Run The Project

1. Build hardware as per `/diagram/`
2. Collect data using CT6B on indoor/outdoor tracks
3. Train your model in Jupyter notebook
4. Deploy `.tflite` model to Raspberry Pi
5. Watch your car drive autonomously 🚗✨

---
