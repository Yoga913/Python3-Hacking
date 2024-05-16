import socket
from IPy import IP

def scan(target):
    converted_ip = check_ip(target)
    print('\n' + '[-_0 Target Pemindaian] ' + str(target))
    for port in range(1,500):
        scan_port(converted_ip, port)

def check_ip(ip):
    try:
        IP(ip)
        return(ip)
    except ValueError:
        return socket.gethostbyname(ip)

def get_banner(s):
    return s.recv(1024)

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ipaddress, port))
        try:
            banner = get_banner(sock)
            print('[+] Buka Port ' + str(port) + ' : ' + str(banner.decode().strip('\n')))
        except:
            print('[+] BUka port ' + str(port))
    except:
        pass


if __name__ == "__main__":
    targets = input('[+] Masukkan Target / s Untuk Memindai (membagi beberapa target dengan ,): ')
    if ',' in targets:
        for ip_add in targets.split(','):
            scan(ip_add.strip(' '))
    else:
        scan(targets)

# ==================================================================================================

# Program ini adalah scanner port sederhana yang memungkinkan pengguna untuk memindai satu atau beberapa target untuk melihat port apa yang terbuka. Berikut adalah penjelasan alur kerjanya:

# 1. **Fungsi `scan(target)`**: Fungsi ini menerima alamat IP target atau nama domain sebagai input. Jika input berupa nama domain, fungsi `check_ip(ip)` akan mengonversinya menjadi alamat IP. Kemudian, fungsi akan mencetak pesan memulai pemindaian untuk target dan memanggil fungsi `scan_port(converted_ip, port)` untuk setiap port dari 1 hingga 500.

# 2. **Fungsi `check_ip(ip)`**: Fungsi ini digunakan untuk memeriksa apakah input yang diberikan adalah alamat IP atau nama domain. Jika input adalah alamat IP yang valid, fungsi akan mengembalikannya; jika bukan, fungsi akan mencoba mengonversi nama domain menjadi alamat IP menggunakan `socket.gethostbyname(ip)`.

# 3. **Fungsi `get_banner(s)`**: Fungsi ini mengambil banner yang dikirim oleh server setelah koneksi berhasil dibuat. Ini digunakan untuk mendapatkan informasi tambahan tentang layanan yang berjalan di port tertentu.

# 4. **Fungsi `scan_port(ipaddress, port)`**: Fungsi ini mencoba membuat koneksi socket ke port yang ditentukan pada alamat IP yang ditentukan. Jika koneksi berhasil, itu mencoba mendapatkan banner dari server dengan memanggil `get_banner(sock)` dan mencetak hasilnya. Jika koneksi gagal, fungsi melewatkannya.

# 5. **Bagian `if __name__ == "__main__":`**: Pada bagian ini, program meminta pengguna untuk memasukkan target atau beberapa target yang akan dipindai. Jika pengguna memasukkan beberapa target, program akan memisahkan target menggunakan tanda koma dan memanggil fungsi `scan` untuk setiap target.

# Dengan cara ini, program memungkinkan pengguna untuk melakukan pemindaian port pada satu atau beberapa target dan mendapatkan informasi tentang port yang terbuka.
