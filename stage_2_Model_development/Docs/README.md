------------
NAVDRIVE - STAGE 2: MODEL DEVELOPMENT
------------

📍 OVERVIEW:
This phase covers the process of transferring collected data from the Raspberry Pi to a PC, preparing it for training, developing a neural network model, and finally converting it into a TensorFlow Lite (TFLite) model for Raspberry Pi deployment.

---

1. TRANSFER DATA TO PC

---

After collecting data on the Raspberry Pi during Phase 1:

1. Connect the Raspberry Pi to your PC via USB or network (SSH/SCP).
2. Transfer the entire dataset directory from Raspberry pi
   to your PC location

---

2. CSV PATH ADJUSTMENT

---

Since the image paths in `data.csv` are configured for the Raspberry Pi, update them to match your PC directory structure.

✔️ Example:

- Old path → `/home/pi/NavDrive/stage_1_data_collection/dataset/raw_images/img1.jpg`
- New path → `C:/NavDrive/dataset/raw_images/img1.jpg`

You can automate this using a Python script

Ensure the modified `data.csv` is saved and verified before proceeding.

---

3. LOADING INTO JUPYTER NOTEBOOK

---

Open the Jupyter Notebook from:

`Model.ipynb`

This notebook includes:

- Data Visualization
- Data Augmentation and Data Preprocessing
- Data cleaning
- Normalization of sensor inputs
- Visualization of steering angles and sensor data

Run the cells step-by-step to verify the data integrity.

---

4. MODEL TRAINING

---

Model training steps include:

- Splitting data into train and validation sets or Test set
- Using a CNN to predict steering angles
- Training with MSE loss and Adam optimizer
- Monitoring loss curves to avoid overfitting

Model is trained for multiple epochs and performance is logged.

📉 Metrics observed:

- Training Loss
- Validation Loss
- Mean Squared Error (MSE)

Once a satisfactory loss level is achieved, save the trained model.

📊 Sample Training Loss Curve:
![](/stage_2_Model_development/Docs/assets/loss.png)

🧠 Sample Predicted Output:
![](/stage_2_Model_development/Docs/assets/sample.png)

---

5. MODEL ARCHITECTURE

---

- Total Parameters: ~100,000
- Layers include: Conv2D, ReLU, MaxPool, Flatten, Dense
- Final layer outputs a single steering angle

Ensure the architecture matches what’s defined in code.

![](/stage_2_Model_development/Docs/assets/model_architecture.png)

---

6. MODEL EXPORT TO TFLITE

---

Convert the trained `.h5` or `.pb` model into TensorFlow Lite format:

The output model:
📁 `model/model.tflite`

This lightweight model is used in Stage 3 on the Raspberry Pi.

---
