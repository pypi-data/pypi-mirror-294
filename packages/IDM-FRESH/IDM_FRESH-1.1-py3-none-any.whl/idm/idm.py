from prettytable import PrettyTable
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

def format_rupiah(amount):
    return f"Rp {amount:,.2f}".replace(".", ",")

# Fungsi untuk memverifikasi lisensi
def verify_license(user_id, license_key):
    secret_key = "kunci_rahasia_anda"
    try:
        license_key, expiration_timestamp = license_key.split('-')
        expiration_timestamp = int(expiration_timestamp)
        if datetime.datetime.now().timestamp() > expiration_timestamp:
            return False
        raw_string = f"{user_id}{expiration_timestamp}{secret_key}"
        expected_key = hashlib.sha256(raw_string.encode()).hexdigest()
        if expected_key != license_key:
            return False
        if not is_license_valid_for_device(license_key):
            return False
        return True
    except (ValueError, IndexError):
        return False

# Fungsi untuk mendapatkan Device ID
def get_device_id():
    return str(uuid.getnode())

# Fungsi untuk memverifikasi apakah lisensi valid untuk perangkat saat ini
def is_license_valid_for_device(license_key):
    device_id = get_device_id()
    if os.path.exists('device_licenses.txt'):
        with open('device_licenses.txt', 'r') as file:
            for line in file:
                saved_license_key, saved_device_id = line.strip().split(',')
                if saved_license_key == license_key:
                    return saved_device_id == device_id
    return True

# Fungsi untuk menyimpan Device ID bersama dengan lisensi
def save_license_for_device(license_key):
    device_id = get_device_id()
    with open('device_licenses.txt', 'a') as file:
        file.write(f"{license_key},{device_id}\n")

# Fungsi untuk meminta user id dan lisensi
def minta_lisensi():
    while True:
        user_id = input("Masukkan User ID: ")
        license_key = input("Masukkan Lisensi (format: key-timestamp): ")
        if verify_license(user_id, license_key):
            save_license_for_device(license_key)
            print("Lisensi berhasil diverifikasi.")
            return True
        else:
            print("Lisensi tidak valid. Silakan coba lagi.")
            return False

# Fungsi untuk memeriksa apakah lisensi sudah pernah dimasukkan sebelumnya
def cek_lisensi_terdaftar():
    if os.path.exists('device_licenses.txt'):
        with open('device_licenses.txt', 'r') as file:
            for line in file:
                if line.strip():
                    return True
    return False

# Fungsi untuk menampilkan stok barang dengan format Rupiah
def tampilkan_stok():
    try:
        with open('stok_barang.txt', 'r') as file:
            table = PrettyTable()
            table.field_names = ["PLU", "NAMA BARANG", "LPPTK", "HARGA (RP)"]
            for line in file:
                data = line.strip().split(',')
                if len(data) < 4:
                    data += ['0'] * (4 - len(data))
                plu, nama_barang, jumlah, harga = data
                harga_rp = format_rupiah(int(harga))
                table.add_row([plu, nama_barang, jumlah, harga_rp])
            
            # Menampilkan tabel dengan efek berjalan
            print("STOK BARANG YANG TELAH DIMASUKKAN:")
            print(table)

    except FileNotFoundError:
        print("BELUM ADA STOK BARANG YANG DIMASUKKAN.")

# Fungsi untuk memasukkan stok barang ke dalam program
def tambah_stok(plu, nama_barang, jumlah, harga):
    with open('stok_barang.txt', 'a') as file:
        file.write(f"{plu},{nama_barang},{jumlah},{harga}\n")

# Fungsi untuk memperbarui stok barang
def perbarui_stok(plu, jumlah_baru):
    try:
        with open('stok_barang.txt', 'r') as file:
            lines = file.readlines()

        with open('stok_barang.txt', 'w') as file:
            updated = False
            for line in lines:
                data = line.strip().split(',')
                if len(data) < 4:
                    data += ['0'] * (4 - len(data))
                current_plu, nama_barang, jumlah, harga = data
                if current_plu == plu:
                    file.write(f"{plu},{nama_barang},{jumlah_baru},{harga}\n")
                    updated = True
                else:
                    file.write(line)

        if updated:
            print(f"STOK UNTUK PLU {plu} BERHASIL DIPERBARUI.")
        else:
            print(f"PLU {plu} TIDAK DITEMUKAN.")

    except FileNotFoundError:
        print("BELUM ADA STOK BARANG YANG DIMASUKKAN.")

# Fungsi untuk memperbarui harga barang dari file
def perbarui_harga_dari_file(nama_file):
    try:
        # Membaca harga baru dari file eksternal
        harga_baru = []
        with open(nama_file, 'r') as file:
            for line in file:
                harga_baru.append(int(line.strip()))

        # Memperbarui harga barang di file stok_fisik.txt
        with open('stok_fisik.txt', 'r') as file:
            lines = file.readlines()

        with open('stok_fisik.txt', 'w') as file:
            for i, line in enumerate(lines):
                if i < len(harga_baru):
                    data = line.strip().split(',')
                    if len(data) >= 4:
                        plu, nama_barang, jumlah, _ = data
                        harga = harga_baru[i]
                        file.write(f"{plu},{nama_barang},{jumlah},{harga}\n")
                    else:
                        file.write(line)
                else:
                    file.write(line)

        print("HARGA BARANG BERHASIL DIPERBARUI DARI FILE.")

    except FileNotFoundError:
        print("FILE TIDAK DITEMUKAN. PASTIKAN NAMA FILE BENAR DAN COBA LAGI.")


# Fungsi untuk membuat file input stok fisik
def buat_file_input_fisik():
    try:
        with open('stok_barang.txt', 'r') as file:
            stok_barang = [line.strip().split(',') for line in file]
            
        with open('stok_fisik.txt', 'w') as file:
            for data in stok_barang:
                if len(data) < 4:
                    data += ['0'] * (4 - len(data))
                plu, nama_barang, _, harga = data
                file.write(f"{plu},{nama_barang},0,{harga}\n")
        
        print("FILE INPUT STOK FISIK TELAH DIBUAT DENGAN NAMA 'stok_fisik.txt'. SILAKAN ISI STOK FISIK BARANG.")

    except FileNotFoundError:
        print("BELUM ADA STOK BARANG YANG DIMASUKKAN.")

# Fungsi untuk memperbarui stok fisik dari file baru
def update_stok_from_file(new_stok_file):
    try:
        with open(new_stok_file, 'r') as new_file:
            new_stok_data = new_file.read().splitlines()

        with open('stok_fisik.txt', 'r') as file:
            lines = file.readlines()

        with open('stok_fisik.txt', 'w') as file:
            for i, line in enumerate(lines):
                data = line.strip().split(',')
                if len(data) < 4:
                    data += ['0'] * (4 - len(data))
                plu, nama_barang, _, harga = data
                if i < len(new_stok_data):
                    jumlah_baru = new_stok_data[i]
                else:
                    jumlah_baru = 0  # Jika file new_stok.txt memiliki lebih sedikit baris
                file.write(f"{plu},{nama_barang},{jumlah_baru},{harga}\n")

        print("Stok berhasil diperbarui dari file baru.")

    except FileNotFoundError:
        print("File tidak ditemukan.")


# Fungsi untuk melakukan opname stok barang
def opname_stok():
    try:
        with open('stok_barang.txt', 'r') as file_stok_barang:
            stok_barang = {line.strip().split(',')[0]: line.strip().split(',') for line in file_stok_barang}

        with open('stok_fisik.txt', 'r') as file_stok_fisik:
            stok_fisik = {line.strip().split(',')[0]: int(line.strip().split(',')[2]) for line in file_stok_fisik}
            
        total_minus = 0
        total_plus = 0
        table_minus = PrettyTable()
        table_plus = PrettyTable()
        table_minus.field_names = ["PLU", "NAMA BARANG", "STOK AWAL", "STOK AKHIR", "SELISIH (Rp)"]
        table_plus.field_names = ["PLU", "NAMA BARANG", "STOK AWAL", "STOK AKHIR", "SELISIH (Rp)"]
        rincian_minus = []
        rincian_plus = []

        for plu, (plu, nama_barang, existing_jumlah, harga) in stok_barang.items():
            existing_jumlah = int(existing_jumlah)
            jumlah_fisik = stok_fisik.get(plu, 0)
            
            if jumlah_fisik > existing_jumlah:
                selisih = (jumlah_fisik - existing_jumlah) * int(harga)
                total_plus += selisih
                table_plus.add_row([plu, nama_barang, existing_jumlah, jumlah_fisik, format_rupiah(selisih)])
                rincian_plus.append(f"{nama_barang} PLUS {jumlah_fisik - existing_jumlah}")
            elif jumlah_fisik < existing_jumlah:
                selisih = (existing_jumlah - jumlah_fisik) * int(harga)
                total_minus += selisih
                table_minus.add_row([plu, nama_barang, existing_jumlah, jumlah_fisik, format_rupiah(selisih)])
                rincian_minus.append(f"{nama_barang} MINUS {existing_jumlah - jumlah_fisik}")

        # Menampilkan tabel minus dengan animasi
        if table_minus.rowcount > 0:
            print("\nTABEL BARANG MINUS:")
            for row in table_minus:
                print(row)
                time.sleep(0.1)  # Menambahkan jeda animasi
            print("\nRINCIAN ITEM MINUS:")
            for rincian in rincian_minus:
                print(rincian)
                time.sleep(0.1)  # Menambahkan jeda animasi

        # Menampilkan tabel plus dengan animasi
        if table_plus.rowcount > 0:
            print("\nTABEL BARANG PLUS:")
            for row in table_plus:
                print(row)
                time.sleep(0.1)  # Menambahkan jeda animasi
            print("\nRINCIAN ITEM PLUS:")
            for rincian in rincian_plus:
                print(rincian)
                time.sleep(0.1)  # Menambahkan jeda animasi

        # Menampilkan total minus dan plus
        print(f"\nTOTAL MINUS: {format_rupiah(total_minus)}")
        print(f"TOTAL PLUS: {format_rupiah(total_plus)}")

        
    except FileNotFoundError:
        print("BELUM ADA STOK BARANG YANG DIMASUKKAN.")
        print("PASTIKAN ANDA TELAH MENGISI FILE 'stok_barang.txt' DAN 'stok_fisik.txt'.")


# Fungsi untuk menunggu pengguna menekan tombol Enter
def tunggu_enter():
    input("ENTER")

# Fungsi untuk menampilkan menu utama
def tampilkan_menu():
    while True:
        os.system('clear')  # Membersihkan layar sebelum menampilkan menu
        print("\n" + "*" * 52)
        print("*          🌟🌟🌟   S T O C K   O P N A M E   🌟🌟🌟          *")
        print("*" * 52)
        print("\n MENU PILIHAN:")
        print("╔═══════════════════════════════════════════════╗")
        print("║ [ 1 ]  🛒 LIHAT STOK BARANG                   ║")
        print("║ [ 2 ]  ➕ TAMBAH STOK BARANG                  ║")
        print("║ [ 3 ]  🔄 PERBARUI STOK BARANG                ║")
        print("║ [ 4 ]  📄 BUAT FILE INPUT STOK FISIK          ║")
        print("║ [ 5 ]  📁 PERBARUI STOK FISIK DARI FILE       ║")
        print("║ [ 6 ]  📊 OPNAME STOK                         ║")
        print("║ [ 7 ]  💲 PERBARUI HARGA BARANG DARI FILE     ║")
        print("║ [ 8 ]  🚪 KELUAR                              ║")
        print("╚═══════════════════════════════════════════════╝")
        print("\n" + "*" * 52)

        pilihan = input("\nPILIH MENU> ")

        if pilihan == "1":
            tampilkan_stok()
            tunggu_enter()
        elif pilihan == "2":
            plu = input("MASUKKAN PLU BARANG: ")
            nama_barang = input("MASUKKAN NAMA BARANG: ")
            jumlah = input("MASUKKAN JUMLAH STOK BARANG: ")
            harga = input("MASUKKAN HARGA BARANG (RP): ")
            tambah_stok(plu, nama_barang, jumlah, harga)
            print("STOK BARANG BERHASIL DITAMBAHKAN.")
            tunggu_enter()
        elif pilihan == "3":
            plu = input("MASUKKAN PLU BARANG YANG AKAN DIPERBARUI: ")
            jumlah_baru = input("MASUKKAN JUMLAH STOK BARU: ")
            perbarui_stok(plu, jumlah_baru)
            tunggu_enter()
        elif pilihan == "4":
            buat_file_input_fisik()
            tunggu_enter()
        elif pilihan == "5":
            file_baru = input("MASUKKAN NAMA FILE BARU UNTUK PERBARUI STOK FISIK: ")
            update_stok_from_file(file_baru)
            tunggu_enter()
        elif pilihan == "6":
            opname_stok()
            tunggu_enter()
        elif pilihan == "7":
            file_harga = input("MASUKKAN NAMA FILE UNTUK PERBARUI HARGA BARANG: ")
            perbarui_harga_dari_file(file_harga)
            tunggu_enter()
        elif pilihan == "8":
            print("TERIMA KASIH TELAH MENGGUNAKAN PROGRAM INI.")
            break
        else:
            print("PILIHAN TIDAK VALID. SILAKAN COBA LAGI.")
            tunggu_enter()

# Cek apakah lisensi sudah terdaftar atau belum, jika belum minta lisensi
if not cek_lisensi_terdaftar():
    if not minta_lisensi():
        exit()

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
def print_berjalan(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Untuk pindah ke baris baru setelah teks selesai dicetak

def print_slow(text):
    """Mencetak teks secara perlahan."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print()
    
def tunggu_enter():
    input("ENTER")
    
def clear_screen():
    """Membersihkan layar."""
    os.system('clear')
    
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

if __name__ == "__main__":
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
                    input("ENTER")

                elif choice == "2":
                    tampilkan_menu()
                    input("ENTER")

                elif choice == "3":
                    days_left = get_license_days_left(license_key)
                    message = f"MASA AKTIF LISENSI ANDA {days_left} HARI LAGI."
                    print_berjalan(message, 0.05)
                    input("ENTER")

                elif choice == "4":
                    print("Keluar...")
                    break

                else:
                    print()
        finally:
            pass
    else:
        print(f"{RED_COLOR}                   LICENSE KEY INVALID!!. ACCESS DENIED.{RESET_COLOR}")
        delete_license_file()
        print(" PLEASE CONTACT ADMIN https://wa.me/6285314247652 FOR YOUR LICENSE.")
