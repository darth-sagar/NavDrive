import time
from datetime import datetime
from camera_handler import CameraHandler
from serial_reader import SerialReader
from data_saver import DataSaver

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
BASE_DIR = 'data_runs'
CAPTURE_RATE = 5  # Target frames per second
CAMERA_ROTATION = 180  # Degrees

def main():
    try:
        # Initialize components
        cam_handler = CameraHandler(
            base_dir=BASE_DIR,
            rotation=CAMERA_ROTATION
        )
        run_folder = cam_handler.create_run_folders()
        
        serial_reader = SerialReader(SERIAL_PORT, BAUD_RATE)
        serial_reader.start_reading()
        
        data_saver = DataSaver(run_folder, cam_handler.run_number)

        print(f"Starting data collection run #{cam_handler.run_number}")
        print(f"Saving to: {run_folder}")
        print(f"Target FPS: {CAPTURE_RATE}")
        print("Press Ctrl+C to stop\n")

        interval = 1.0 / CAPTURE_RATE
        next_capture = time.time()
        capture_count = 0
        status_interval = 2
        start_time = time.time()
        last_status = time.time()

        while True:
            now = time.time()
            if now >= next_capture:
                # Get fresh sensor data
                with serial_reader.lock:
                    data = serial_reader.latest_data.copy()

                # Capture and save image
                img_path = cam_handler.capture_image()
                timestamp = datetime.now().isoformat()

                if img_path:
                    # Save to CSV
                    try:
                        data_saver.add_entry(timestamp, img_path, data)
                        capture_count += 1
                    except Exception as e:
                        print(f" CSV save error: {e}")

                # Calculate actual FPS
                elapsed = time.time() - start_time
                if elapsed >= 5:  # Update every 5 seconds
                    elapsed = now - start_time
                    actual_fps = capture_count / elapsed
                    print(f""
                          f""
                          f"Throttle: {data.get('throttle', 0.0):.2f} | "
                          f"Steering: {data.get('steering', 0.0):.2f}")
                    last_status = now
                    start_time = time.time()
                    capture_count = 0

                # Maintain capture rate
                next_capture += interval
                remaining = next_capture - time.time()
                if remaining > 0:
                    time.sleep(remaining * 0.9)  # Compensate for processing time

    except KeyboardInterrupt:
        print("\nUser requested shutdown...")
    except Exception as e:
        print(f"\n Critical error: {str(e)}")
    finally:
        print("\n Cleaning up resources...")
        serial_reader.stop_reading()
        data_saver.close()
        cam_handler.close()
        print(f"Run {cam_handler.run_number} complete")

if __name__ == "__main__":
    main()