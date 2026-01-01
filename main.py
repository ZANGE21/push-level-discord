import requests
import time
import os 

def get_last_message_id(channel_id, headers, target_user_id):                                                       r = requests.get(
        f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=5",
        headers=headers
    )
    if r.status_code == 200:
        for msg in r.json():
            if msg["author"]["id"] == target_user_id:
                return msg["id"]
    return None

# Banner
os.system('clear')
print(r"""
███████╗ █████╗ ███╗   ██╗ ██████╗
╚══███╔╝██╔══██╗████╗  ██║██╔════╝
  ███╔╝ ███████║██╔██╗ ██║██║  ███╗
 ███╔╝  ██╔══██║██║╚██╗██║██║   ██║
███████╗██║  ██║██║ ╚████║╚██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝
Push Discord Bot - Lock one user
""")

# Input
channel_id = input("Masukkan ID channel: ")
waktu_kirim = int(input("Set Waktu Kirim Pesan (detik): "))
MY_USER_ID = "1416495302143119452"
TARGET_USER_ID = "1224798953371992208"

# Clear screen
os.system('clear')

# Read token
with open("token.txt", "r") as f:
    token = f.read().strip()

# Read messages
with open("pesan.txt", "r") as f:
    messages = f.readlines()
index = 0

headers = {
    "authorization": token
}

print("[+] Bot berjalan...")
print("[+] Tekan CTRL + C untuk berhenti\n")

# Loop kirim pesan
while True:
    try:
        last_id = get_last_message_id(channel_id, headers, TARGET_USER_ID)

        if last_id:
            payload = {
                "content": messages[index].strip(),
                "message_reference": {
                    "message_id": last_id
                }
            }
        else:
            # kalau target belum chat → kirim biasa / bisa juga di-skip
            payload = {
                "content": messages[index].strip()
            }

        r = requests.post(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            json=payload
        )

        if r.status_code == 200:
            print(f"[✓] Pesan terkirim: {messages[index].strip()}")
        else:
            print(f"[x] Gagal kirim pesan | Status: {r.status_code}")

        index += 1
        if index >= len(messages):
            index = 0

        time.sleep(waktu_kirim)

    except KeyboardInterrupt:
        print("\n[!] Bot dihentikan")
        break
