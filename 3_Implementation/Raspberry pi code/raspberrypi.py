import cv2
import subprocess
import numpy as np
import tflite_runtime.interpreter as tflite

# === Load TFLite Model ===
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']  # Should be [1, 66, 200, 3]

# === Start Pi Camera via libcamera-vid stream ===
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

print("?? NavDrive is predicting steering... Press Ctrl+C to stop.")
buffer = b""

try:
    while True:
        chunk = process.stdout.read(1024)
        if not chunk:
            break
        buffer += chunk

        # Look for JPEG image markers
        start = buffer.find(b"\xff\xd8")
        end = buffer.find(b"\xff\xd9")

        if start != -1 and end != -1 and end > start:
            jpg = buffer[start:end + 2]
            buffer = buffer[end + 2:]

            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                continue

            # Resize to 200x66 (width x height)
            input_img = cv2.resize(image, (200, 66))
            input_img = input_img.astype(np.float32) / 255.0  # Normalize
            input_img = np.expand_dims(input_img, axis=0)     # Shape: [1, 66, 200, 3]

            # Feed into model
            interpreter.set_tensor(input_details[0]['index'], input_img)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])

            predicted_steering = output_data[0]  # Adjust this if output shape differs
            print(f"?? Predicted Steering Angle: {predicted_steering}")


except KeyboardInterrupt:
    print("? Exiting...")

finally:
    process.terminate()
    cv2.destroyAllWindows()

