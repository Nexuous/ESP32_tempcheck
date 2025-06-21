import time
import socket

ESP32_IP = '192.168.4.1'   # Change to your ESP32's IP address
ESP32_PORT = 8080          # Change to your ESP32's listening port

def connect_esp32(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            print("Connected to ESP32 over WiFi.")
            return s
        except socket.error:
            print("ESP32 not found. Retrying in 2 seconds...")
            time.sleep(2)

def get_temp_humidity(sock):
    try:
        sock.sendall(b'READ\n')  # Command ESP32 to send data
        data = sock.recv(1024).decode().strip()
        if data:
            try:
                temp, hum = map(float, data.split(','))
                return temp, hum
            except ValueError:
                print("Invalid data received:", data)
    except socket.error as e:
        print("Socket error:", e)
    return None, None

def main():
    sock = connect_esp32(ESP32_IP, ESP32_PORT)
    try:
        while True:
            temp, hum = get_temp_humidity(sock)
            if temp is not None and hum is not None:
                print(f"Temperature: {temp}°C, Humidity: {hum}%")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()