import threading
from picamera2 import Picamera2
from pathlib import Path
import time
from datetime import datetime

class CameraHandler:
    def __init__(self, base_dir='data_runs', resolution=(640, 480), rotation=180):
        self.base_dir = Path(base_dir)
        self.resolution = resolution
        self.rotation = rotation  # Store rotation parameter
        self.current_run_folder = None
        self.run_number = self._get_next_run_number()
        self.lock = threading.Lock()
        self.picam2 = None
        self._initialize_camera()
        
        
    def _initialize_camera(self):
        try:
            self.picam2 = Picamera2()
            self.picam2.rotation = self.rotation
            config = self.picam2.create_still_configuration(
                main={"size": self.resolution},
                buffer_count=6  # Better for continuous capture
            )
            self.picam2.configure(config)
            self.picam2.start()  # Keep camera warm
            time.sleep(2)  # Initial warmup
        except Exception as e:
            raise RuntimeError(f"Camera initialization failed: {str(e)}")

    def _get_next_run_number(self):
        try:
            existing_runs = [int(d.name.split('_')[1]) for d in self.base_dir.glob('run_*') if d.is_dir()]
            return max(existing_runs) + 1 if existing_runs else 0
        except Exception as e:
            raise RuntimeError(f"Run numbering error: {str(e)}")

    def create_run_folders(self):
        try:
            self.current_run_folder = self.base_dir / f"run_{self.run_number:04d}"
            (self.current_run_folder / 'images').mkdir(parents=True, exist_ok=True)
            (self.current_run_folder / 'csv').mkdir(parents=True, exist_ok=True)
            return self.current_run_folder
        except Exception as e:
            raise RuntimeError(f"Folder creation failed: {str(e)}")

    def capture_image(self):
        if self.current_run_folder is None:
            raise RuntimeError("Run folder not initialized")
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"run_{self.run_number:04d}_{timestamp}.jpg"
            img_path = self.current_run_folder / 'images' / filename
            
            
            with self.lock:
                
                self.picam2.capture_file(str(img_path))

            

            return str(img_path.relative_to(self.base_dir))
        except Exception as e:
            print(f"Capture failed: {str(e)}")
            return None
        
    

    def close(self):
        if self.picam2 is not None:
            self.picam2.stop()
            self.picam2.close()









"""import threading
from picamera2 import Picamera2
from pathlib import Path
import time
from datetime import datetime

BASE_DIR = 'data_runs'


class CameraHandler:
    def __init__(self, resolution=(640, 480)):
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration(main={"size": resolution})
        self.picam2.configure(config)
        self.current_run_folder = None
        self.run_number = self._get_next_run_number()
        self.lock = threading.Lock()

    def _get_next_run_number(self):
        existing_runs = [d.name for d in Path(BASE_DIR).glob('run_*') if d.is_dir()]
        return len(existing_runs)

    def create_run_folders(self):
        self.current_run_folder = Path(BASE_DIR) / f"run_{self.run_number}"
        (self.current_run_folder / 'images').mkdir(parents=True, exist_ok=True)
        (self.current_run_folder / 'csv').mkdir(parents=True, exist_ok=True)
        return self.current_run_folder

    def capture_image(self):
        if self.current_run_folder is None:
            raise Exception("Run folder not created")

        timestamp = datetime.now().strftime("%d_%H%M%S%f")
        filename = f"img_{self.run_number}_{timestamp}.jpg"
        img_folder = self.current_run_folder / 'images'
        path = img_folder / filename

        with self.lock:
            self.picam2.start()
            time.sleep(0.1)  # Camera warm-up
            self.picam2.capture_file(str(path))
            self.picam2.stop()

        return str(path.relative_to(BASE_DIR))
    def close(self):
        self.picam2.close()"""