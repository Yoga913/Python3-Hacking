import socket
import os

#  1. **Perpustakaan Impor:**
 # Program dimulai dengan mengimpor dua modul dari pustaka standar Python, yaitu 'socket' dan 'os'. Modul 'socket' digunakan untuk membuat dan mengendalikan soket (socket) jaringan, sedangkan modul 'os' digunakan untuk berinteraksi dengan sistem operasi.

# host to listen on
host = "192.168.0.196"

# 2. **Penetapan Host:**
#  Variabel 'host' ditetapkan dengan alamat IP host yang ingin didengarkan. Ini adalah alamat IP yang akan diawasi oleh sniffer.

# create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol) 

sniffer.bind((host, 0))
#3. **Membuat Soket:**
#  Program membuat sebuah soket (socket) menggunakan fungsi 'socket.socket()'. Jenis soket yang dibuat adalah soket mentah (raw socket), yang memungkinkan program untuk mengakses dan memproses data lalu lintas jaringan secara langsung.
 

# we want the IP headers included in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# 4. **Pengikatan Soket:**
# Soket yang telah dibuat kemudian diikat (bind) dengan alamat IP host dan nomor port tertentu. Dalam contoh ini, nomor port tidak ditentukan secara spesifik (0), sehingga sistem akan memilih nomor port secara otomatis.

# if we're on Windows we need to send an IOCTL
# to setup promiscuous mode
if os.name == "nt": 
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# read in a single packet
print(sniffer.recvfrom(65535))

# if we're on Windows turn off promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


# =================================================================== # 

# Program yang Anda bagikan adalah contoh kode Python untuk membuat sebuah sniffer jaringan yang dapat mendengarkan lalu lintas jaringan yang masuk.
# **Menyenangkan
# Cara Penggunaan:

# Pengguna harus mengetahui alamat IP host yang ingin didengarkan. Informasi ini harus diperbarui di dalam kode dengan mengganti nilai variabel 'ho
# Setelah pria
# Hasil dari lalu lintas yang didengarkan akan dicetak di terminal pengguna.

# Pengembangan:
# Program ini dapat dikembangkan lebih lanjut dengan menambahkan fitur-fitur seperti:
# Mengurai da
# Pena
# Implementasi filter untuk memungkinkan penggunaan hanya untuk memantau atau merekam lalu lintas yang spesifik.
# Antarmuka pengguna grafis (GUI) untuk pengaturan dan visualisasi data yang lebih mudah dimengerti.
# Selain itu, perlu diingat bahwa penggunaan sniffer jaringan memerlukan pengetahuan yang cukup tentang protokol jaringan, keamanan, dan privasi. Pengembangan lebih lanjut harus memperhitungkan aspek-aspek tersebut.
# Sebagai catatan, penggunaan sniffer jaringan juga seringkali terkait dengan kegiatan yang mengikuti regulasi tertentu dan etika yang berlaku, seperti privasi pengguna dan aturan-aturan penggunaan jaringan. Sebelum digunakan dalam lingkungan yang sensitif, pastikan untuk memahami persyaratan hukum dan kebijakan yang berlaku.


# berikut adalah penjelasan mengenai alur program di atas adalah :
# 1. **Perpustakaan Impor:**
# program dimulai dengan mengimpor dua modul dari pustaka standar Python, yaitu 'socket' dan 'os'. Modul 'socket' digunakan untuk membuat dan mengendalikan soket (socket) jaringan, sedangkan modul 'os' digunakan untuk berinteraksi dengan sistem operasi.

# 2. **Penetapan Host:**
#  Variabel 'host' ditetapkan dengan alamat IP host yang ingin didengarkan. Ini adalah alamat IP yang akan diawasi oleh sniffer.

# 3. **Membuat Soket:**
#  Program membuat sebuah soket (socket) menggunakan fungsi 'socket.socket()'. Jenis soket yang dibuat adalah soket mentah (raw socket), yang memungkinkan program untuk mengakses dan memproses data lalu lintas jaringan secara langsung.

# 4. **Pengikatan Soket:**
#  Soket yang telah dibuat kemudian diikat (bind) dengan alamat IP host dan nomor port tertentu. Dalam contoh ini, nomor port tidak ditentukan secara spesifik (0), sehingga sistem akan memilih nomor port secara otomatis.

# 5. **Mengatur Opsi Soket:**
#  Sniffer diatur untuk menyertakan header IP dalam tangkapan data dengan menggunakan metode 'setsockopt()'. Ini memungkinkan program untuk memproses paket data jaringan secara lengkap, termasuk header IP.

# 6. **Mengaktifkan Mode Promiskuitas (Hanya pada Windows):**
#  Jika sistem operasi yang digunakan adalah Windows, program akan mengatur soket dalam mode promiskuitas menggunakan 'ioctl()' dengan konstanta 'SIO_RCVALL' dan 'RCVALL_ON'. Mode promiskuitas memungkinkan sniffer untuk menangkap semua paket yang melewati antarmuka jaringan, bukan hanya paket yang ditujukan untuk host tertentu.

# 7. **Mendengarkan Paket:**
#  Program menggunakan metode 'recvfrom()' untuk menerima paket data yang masuk melalui soket. Fungsi ini akan memblokir program sampai ada paket yang diterima atau waktu tertentu telah berlalu.

# 8. **Cetak Data Paket:**
#  Paket data yang diterima dicetak ke terminal pengguna menggunakan fungsi 'print()'.

# 9. **Menonaktifkan Mode Promiskuitas (Hanya pada Windows):**
#  Jika program berjalan di sistem Windows, setelah selesai mendengarkan, program akan menonaktifkan mode promiskuitas dengan menggunakan 'ioctl()' dengan konstanta 'SIO_RCVALL' dan 'RCVALL_OFF'.

# Demikianlah, itu adalah alur program yang mencakup langkah-langkah dari mulai membuat soket untuk mendengarkan lalu lintas jaringan hingga mencetak data paket yang diterima.



