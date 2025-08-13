import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import threading
import time
import subprocess
from collections import deque

# Load TFLite Model
interpreter = tflite.Interpreter(model_path="04_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Globals
frame_lock = threading.Lock()cc
frame_buffer = deque(maxlen=1)
prediction_result = [0.0]
fps = [0.0]
reward = [0.0]

# Reward Function
def calculate_reward(predicted_steering):
    distance_from_center = abs(predicted_steering)
    r = max(0.0, 1.0 - distance_from_center)
    return r

# Thread: Frame Reader
def stream_reader():
    cmd = [
        "libcamera-vid",
        "--width", "200",
        "--height", "66",
        "--framerate", "30",
        "--codec", "mjpeg",
        "--inline",
        "-o", "-",
        "--nopreview",
        "--timeout", "0"
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    buffer = b""
    try:
        while True:
            chunk = process.stdout.read(1024)
            if not chunk:
                break
            buffer += chunk
            start = buffer.find(b"\xff\xd8")
            end = buffer.find(b"\xff\xd9")
            if start != -1 and end != -1 and end > start:
                jpg = buffer[start:end + 2]
                buffer = buffer[end + 2:]
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if img is not None:
                    with frame_lock:
                        frame_buffer.append(img)
    except Exception as e:
        print("Error in stream_reader:", e)
    finally:
        process.terminate()

# Thread: Inference + Visualization
def inference_loop():
    last_time = time.time()
    while True:
        with frame_lock:
            if not frame_buffer:
                continue
            frame = frame_buffer[-1].copy()

        input_img = cv2.resize(frame, (200, 66)).astype(np.float32) / 255.0
        input_img = np.expand_dims(input_img, axis=0)

        interpreter.set_tensor(input_details[0]['index'], input_img)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]['index'])
        predicted_steering = float(output[0])
        prediction_result[0] = predicted_steering

        current_time = time.time()
        fps[0] = 1.0 / (current_time - last_time)
        last_time = current_time

        reward[0] = calculate_reward(predicted_steering)

        overlay = frame.copy()
        h, w, _ = overlay.shape
        center_x = w // 2

        cv2.line(overlay, (center_x, 0), (center_x, h), (255, 255, 255), 2)

        pred_x = int((predicted_steering + 1) / 2 * w)
        cv2.line(overlay, (pred_x, 0), (pred_x, h), (0, 255, 0), 2)

        cv2.putText(overlay, f"Steering: {predicted_steering:+.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 255, 50), 2)
        cv2.putText(overlay, f"Reward: {reward[0]:.2f}", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
        cv2.putText(overlay, f"FPS: {fps[0]:.1f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

        cv2.imshow("NavDrive - Live Inference", overlay)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Start Threads
print("NavDrive multithreaded prediction started... Press 'q' to quit.")
threading.Thread(target=stream_reader, daemon=True).start()
inference_loop()
