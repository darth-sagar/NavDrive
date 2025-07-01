import csv
import threading
from pathlib import Path

class DataSaver:
    def __init__(self, folder, run_number):
        self.run_folder = Path(folder)
        self.csv_path = self.run_folder / f"run_{run_number:04d}.csv"
        self.lock = threading.Lock()
        self._initialize_csv()
        
    def _initialize_csv(self):
        try:
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp',
                    'image_path', 
                    'throttle',
                    'steering'
                ])
        except Exception as e:
            raise RuntimeError(f"CSV init failed: {str(e)}")

    def add_entry(self, timestamp, image_path, data):
        if not image_path:
            return
            
        try:
            # Convert absolute path to run-folder-relative path
            abs_img_path = self.run_folder.parent / image_path
            rel_img_path = abs_img_path.relative_to(self.run_folder)
            
            with self.lock, open(self.csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    str(rel_img_path),
                    data.get('throttle', 0.0),
                    data.get('steering', 0.0)
                ])
        except Exception as e:
            print(f"CSV write error: {str(e)}")

    def close(self):
        pass