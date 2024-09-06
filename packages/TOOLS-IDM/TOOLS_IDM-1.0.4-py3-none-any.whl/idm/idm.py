import hashlib
import datetime
import barcode
from barcode.writer import ImageWriter
import os
import time
import uuid
import subprocess
import sys

# Konstanta
SECRET_KEY = "kunci_rahasia_anda"
USER_LICENSE_FILE = 'user_license.txt'
DEVICE_LICENSE_FILE = 'device_license.txt'
INPUT_FILE = "input.txt"
BLUE_COLOR = "\033[94m"
GREEN_COLOR = "\033[92m"
CYAN_COLOR = "\033[96m"
RED_COLOR = "\033[91m"
YELLOW_COLOR = "\033[93m"
MAGENTA_COLOR = "\033[95m"
RESET_COLOR = "\033[0m"

# ========== Bagian Lisensi ==========

def verify_license(user_id, license_key):
    """Memverifikasi lisensi pengguna."""
    try:
        license_key, expiration_timestamp = license_key.split('-')
        expiration_timestamp = int(expiration_timestamp)
        if datetime.datetime.now().timestamp() > expiration_timestamp:
            delete_license_file()
            return False
        raw_string = f"{user_id}{expiration_timestamp}{SECRET_KEY}"
        expected_key = hashlib.sha256(raw_string.encode()).hexdigest()
        if expected_key != license_key:
            return False
        if not is_license_valid_for_device(license_key):
            return False
        return True
    except (ValueError, IndexError):
        return False

def delete_license_file():
    """Menghapus file lisensi pengguna."""
    if os.path.exists(USER_LICENSE_FILE):
        os.remove(USER_LICENSE_FILE)

def get_device_id():
    """Menghasilkan UUID acak sebagai Device ID."""
    return str(uuid.uuid4())

def is_license_valid_for_device(license_key):
    """Memverifikasi apakah lisensi valid untuk perangkat saat ini."""
    device_id = get_device_id()
    if os.path.exists(DEVICE_LICENSE_FILE):
        with open(DEVICE_LICENSE_FILE, 'r') as file:
            for line in file:
                saved_license_key, saved_device_id = line.strip().split(',')
                if saved_license_key == license_key:
                    return saved_device_id == device_id
    return True

def save_license_for_device(license_key):
    """Menyimpan Device ID bersama dengan lisensi."""
    device_id = get_device_id()
    with open(DEVICE_LICENSE_FILE, 'a') as file:
        file.write(f"{license_key},{device_id}\n")

def get_license_days_left(license_key):
    """Menghitung sisa waktu lisensi dalam hari."""
    try:
        _, expiration_timestamp = license_key.split('-')
        expiration_timestamp = int(expiration_timestamp)
        current_timestamp = datetime.datetime.now().timestamp()
        days_left = (expiration_timestamp - current_timestamp) / (60 * 60 * 24)
        return max(0, int(days_left))
    except (ValueError, IndexError):
        return 0

def save_license_info(user_id, license_key):
    """Menyimpan informasi lisensi pengguna."""
    with open(USER_LICENSE_FILE, 'w') as file:
        file.write(f"{user_id}\n{license_key}")

def load_license_info():
    """Memuat informasi lisensi pengguna."""
    if os.path.exists(USER_LICENSE_FILE):
        with open(USER_LICENSE_FILE, 'r') as file:
            user_id = file.readline().strip()
            license_key = file.readline().strip()
            return user_id, license_key
    return None, None

# ========== Bagian Barcode ==========

def generate_code128_barcode(text, barcode_size, output_dir):
    """Menghasilkan barcode Code128 dan menyimpannya ke direktori output."""
    options = {
        'module_height': barcode_size,
        'module_width': 1,
        'quiet_zone': 15,
        'text_distance': 5,
        'font_size': 10,
        'background': 'white',
        'foreground': 'black'
    }
    code128 = barcode.get('code128', text, writer=ImageWriter())
    filename = os.path.join(output_dir, f'{text}.png')
    code128.save(filename, options)
    print(f"\b BARCODE UNTUK '{text}' BERHASIL DIBUAT DAN DISIMPAN SEBAGAI {filename}")

def read_plu_from_file(filename):
    """Membaca PLU dari file dan mengembalikan daftar PLU."""
    plu_list = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                plu = line.strip()
                if plu:
                    plu_list.append(plu)
    else:
        print(f"File {filename} tidak ditemukan.")
    return plu_list

# ========== Bagian Utilitas ==========

def print_slow(text):
    """Mencetak teks secara perlahan."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

def clear_screen():
    """Membersihkan layar."""
    os.system('clear')

def panggil_script_kedua():
    """Memanggil script kedua."""
    subprocess.run(["python", "so.py"])

# ========== Bagian Menu ==========

def display_menu():
    """Menampilkan menu utama."""
    lines = [
        "  ____   ___  ____  ______   __  _ _____ ",
        " |  _ \\ / _ \\| __ )| __ ) \\ / / / |___ / ",
        " | |_) | | | |  _ \\|  _ \\\\ V /   | | |_ \\ ",
        " |  _ <| |_| | |_) | |_) || |   | |___) |",
        " |_| \\_\\___/|____/|____/ |_|    |_|____/ "
    ]

    print_slow(f"{BLUE_COLOR} ╔════════════════════════════════════════╗{RESET_COLOR}")
    for line in lines:
        print_slow(f"{CYAN_COLOR} {line} {RESET_COLOR}")
    print_slow(f"{YELLOW_COLOR}               IDM | {RED_COLOR}V2.3.0{RESET_COLOR}")
    print_slow(f"{BLUE_COLOR} ╚════════════════════════════════════════╝{RESET_COLOR}")
    print()

    print(f"{YELLOW_COLOR}   *** MENU SCRIPT INDOMARET ***{RESET_COLOR}")
    print(f"{YELLOW_COLOR}==========================================={RESET_COLOR}")
    
    menu_items = [
        "[1] 📝  GENERATE BARCODE",
        "[2] 📦  STOCK OPNAME (MAINTENANCE)",
        "[3] 🔑  MASA AKTIF LISENSI",
        "[4] ❌  EXIT"
    ]
    
    for item in menu_items:
        print(f"{GREEN_COLOR}{item}{RESET_COLOR}")
    
    print(f"{YELLOW_COLOR}==========================================={RESET_COLOR}")
    
    choice = input(f"{GREEN_COLOR}PILIH MENU: {RESET_COLOR}")
    return choice

def handle_generate_barcode():
    """Menangani submenu untuk menghasilkan barcode."""
    print(f"{YELLOW_COLOR}==========================================={RESET_COLOR}")
    print(f"{GREEN_COLOR}[1] BARCODE ITT{RESET_COLOR}")
    print(f"{GREEN_COLOR}[2] PLU PERUBAHAN HARGA{RESET_COLOR}")
    print(f"{YELLOW_COLOR}==========================================={RESET_COLOR}")

    submenu_choice = input(f"{GREEN_COLOR}PILIH SUB-MENU: {RESET_COLOR}")

    barcode_size = input(f"{CYAN_COLOR}MASUKKAN SIZE BARCODE (mm): {RESET_COLOR}")
    try:
        barcode_size = float(barcode_size)
    except ValueError:
        print(f"{RED_COLOR}Ukuran barcode tidak valid. Harap masukkan angka.{RESET_COLOR}")
        return

    if submenu_choice == "1":
        output_dir = "ITT"
    elif submenu_choice == "2":
        output_dir = "MONITORING"
    else:
        print(f"{RED_COLOR}Pilihan tidak valid. Silakan masukkan 1 atau 2.{RESET_COLOR}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plu_list = read_plu_from_file(INPUT_FILE)

    for plu in plu_list:
        generate_code128_barcode(plu, barcode_size, output_dir)

# ========== Fungsi Utama ==========

def main():
    clear_screen()
    
    user_id, license_key = load_license_info()

    if user_id is None or license_key is None:
        device_id = get_device_id()
        print(f"DEVICE ID ANDA: {device_id}")
        user_id = input(" USER ID : ")
        license_key = input(" LICENSE KEY : ")
        save_license_info(user_id, license_key)
        save_license_for_device(license_key)

    if verify_license(user_id, license_key):
        print("              LICENSE KEY VALID!.")
        try:
            while True:
                choice = display_menu()

                if choice == "1":
                    handle_generate_barcode()

                elif choice == "2":
                    panggil_script_kedua()

                elif choice == "3":
                    days_left = get_license_days_left(license_key)
                    print(f"MASA AKTIF LISENSI ANDA {days_left} HARI LAGI.")

                elif choice == "4":
                    print("Keluar...")
                    break

                else:
                    print("Pilihan tidak valid. Silakan masukkan 1, 2, 3, atau 4.")
        finally:
            pass
    else:
        print(f"{RED_COLOR}                   LICENSE KEY INVALID!!. ACCESS DENIED.{RESET_COLOR}")
        delete_license_file()
        print(" PLEASE CONTACT ADMIN https://wa.me/6285314247652 FOR YOUR LICENSE.")

if __name__ == "__main__":
    main()