import serial
import datetime
import requests

COM_PORT = "COM3"
BAUD_RATES = 9600
SERVER_URL = "https://narrativelab.org/cgi-bin/workspace-monitor.py"
UPDATE_INTERVAL = 50 # seconds
DEBUG = False

def main():
    serial_port = serial.Serial(COM_PORT, BAUD_RATES, timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    print(f"COM port: {serial_port.portstr}")
    try:
        records = []
        # record current time, to count one minute of records
        start_time = datetime.datetime.now()
        while True:
            line = serial_port.readline().decode('utf-8').strip()
            print(line)
            splits = line.split(";")
            id = int(splits[0])
            sensor_type = splits[1]
            value = int(splits[2])
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            json_record = {
                "sensorid": id,
                "sensortype": sensor_type,
                "value": value,
                "timestamp": now
            }
            records.append(json_record)

            # if one minute has passed, post to server
            current_time = datetime.datetime.now()
            if (current_time - start_time).total_seconds() >= UPDATE_INTERVAL:
                print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} Posting to server...")
                requests.post(SERVER_URL, json=records)
                records = []
                start_time = datetime.datetime.now()

            if DEBUG:
                print(json_record)
    except KeyboardInterrupt:
        serial_port.close()
        print("Serial port closed")

if __name__ == "__main__":
    main()
