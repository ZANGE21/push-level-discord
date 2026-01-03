import requests
import time
import os
import random

def send_typing(channel_id, headers):
    try:
        requests.post(
            f"https://discord.com/api/v9/channels/{channel_id}/typing",
            headers=headers,
            timeout=10
        )
    except:
        pass

def get_last_message_id(channel_id, headers, target_user_id):
    r = requests.get(
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
MY_USER_ID = "ISI TOKEN LO DISINI"
TARGET_USER_ID = "TOKEN TARGET"

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

# Loop kirim pesan by Zang
last_replied_id = None

while True:
    try:
        last_id = get_last_message_id(channel_id, headers, TARGET_USER_ID)

        # ada pesan baru dari target & belum pernah dibalas
        if last_id and last_id != last_replied_id:
            payload = {
                "content": messages[index].strip(),
                "message_reference": {
                    "message_id": last_id
                },
                "allowed_mentions": {"replied_user": False}
            }

            # typing indicator
            send_typing(channel_id, headers)
            time.sleep(random.randint(4, 7))

            r = requests.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=headers,
                json=payload,
                timeout=10
            )

            if r.status_code == 200:
                print(f"[✓] Reply terkirim: {messages[index].strip()}")
                last_replied_id = last_id
                index = (index + 1) % len(messages)
                time.sleep(waktu_kirim)
            else:
                print(f"[x] Gagal kirim pesan | Status: {r.status_code}")
                time.sleep(10)

        else:
            # belum ada pesan baru dari target
            time.sleep(21)

    except KeyboardInterrupt:
        print("\n[!] Bot dihentikan")
        break

    except requests.exceptions.RequestException as e:
        print(f"[!] Network error: {e}")
        time.sleep(15)
