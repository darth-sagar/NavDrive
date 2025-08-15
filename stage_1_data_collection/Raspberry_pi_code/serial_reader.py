import serial
import threading

SERIAL_TIMEOUT = 1 

class SerialReader:
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate, timeout=SERIAL_TIMEOUT)
        self.latest_data = {'throttle': 0.0, 'steering': 0.0}
        self.running = True
        self.lock = threading.Lock()

    def start_reading(self):
        self.thread = threading.Thread(target=self._read_loop)
        self.thread.start()

    def _read_loop(self):
        while self.running:
            try:
                raw_data=self.ser.readline()
                line=raw_data.decode(errors="replace").strip()
                #print(f"[raw hex]{raw_data.hex()}")
                #print(f"[raw line] Raw line: {line}")
                if line:
                    #print(f"[DEBUG] Parsed data: {self.latest_data}")
                   # print(f"[Serial] {line}")   #for debbugging purpose
                    self._parse_data(line)
            except Exception as e:
                print(f"Serial error: {e}")

    def _parse_data(self,line):
        parsed={}
        try:
            line = line.strip().replace(' ', '')
            for part in line.split('|'):
                if ':' in part:
                     key, value = part.split(':', 1)
                     key = key.lower()  # Convert to lowercase
                    
                     if key == 'throttle':
                         
                         parsed['throttle'] = float(value)
                     elif key == 'steering':
                         parsed['steering'] = float(value)
            with self.lock:
                self.latest_data.update(parsed)
        except exception as e:
            print(f"parse error : {e}")
            
    def stop_reading(self):
        self.running=False
        self.thread.join()
        self.ser.close()


