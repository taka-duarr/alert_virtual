import socket, json, time, requests, threading

SERVER_IP = "127.0.0.1"

# ambil token otomatis
resp = requests.get(f"http://{SERVER_IP}:8080/token")
TOKEN = resp.json()["token"]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# variabel suhu global
suhu = 30

print("🚀 Sensor berjalan (kirim tiap 1 detik)")
print("Ketik suhu baru lalu ENTER untuk mengubah")
print("Tekan Ctrl+C untuk berhenti")

# ======================
# THREAD INPUT SUHU
# ======================
def input_suhu():
    global suhu
    while True:
        try:
            new_suhu = int(input("➡️ Set suhu baru (°C): "))
            suhu = new_suhu
            print(f"✅ Suhu diubah menjadi {suhu}°C")
        except ValueError:
            print("❌ Masukkan angka!")

# ======================
# THREAD KIRIM UDP
# ======================
def send_udp():
    while True:
        payload = {
            "token": TOKEN,
            "device_id": "Gedung H Ruang H3 405",
            "temperature": suhu
        }

        sock.sendto(json.dumps(payload).encode(), (SERVER_IP, 9999))
        print(f"📡 UDP terkirim: {suhu}°C")

        time.sleep(1)

# jalankan thread
threading.Thread(target=input_suhu, daemon=True).start()
send_udp()
