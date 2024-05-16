import socket
import os
import struct
from ctypes import *

# host to listen on
host = "192.168.0.187"


class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_uint32),
        ("dst", c_uint32)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.socket_buffer = socket_buffer

        # map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))

        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except IndexError:
            self.protocol = str(self.protocol_num)


# create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

# we want the IP headers included in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# if we're on Windows we need to send some ioctl
# to setup promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        # read in a single packet
        raw_buffer = sniffer.recvfrom(65535)[0]

        # create an IP header from the first 20 bytes of the buffer
        ip_header = IP(raw_buffer[:20])

        print("Protocol: %s %s -> %s" % (
            ip_header.protocol,
            ip_header.src_address,
            ip_header.dst_address)
              )

except KeyboardInterrupt:
    # if we're on Windows turn off promiscuous mode
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

# ==================================================================================== # 
        
# Program tersebut adalah sebuah alat sederhana untuk mendengarkan lalu lintas jaringan pada sebuah host. Ini memungkinkan Anda untuk menangkap paket data yang melewati host tersebut dan mengekstrak informasi dasar dari header IP dari paket tersebut.

# Berikut adalah alur programnya:

# Import Libraries: Program mengimpor modul-modul yang diperlukan, seperti socket, os, struct, dan ctypes.

# Inisialisasi Variabel: Program menentukan host yang akan didengarkan untuk lalu lintas jaringan. Variabel host ditetapkan sebagai alamat IP tujuan.

# Membuat Struktur IP: Program mendefinisikan sebuah struktur yang merepresentasikan header IP. Ini dilakukan dengan menggunakan modul ctypes. Struktur ini memiliki atribut-atribut yang merepresentasikan berbagai bagian dari header IP.

# Membuat Socket: Program membuat sebuah socket raw dengan menggunakan socket.socket(). Socket ini akan digunakan untuk menangkap paket-paket jaringan.

# Mengikat Socket: Socket diikat ke host yang ditentukan dan port 0, yang berarti bahwa socket ini akan menangkap semua paket yang tiba ke host tersebut.

# Mengatur Opsi Socket: Program mengatur opsi socket sehingga header IP akan disertakan dalam data yang diterima. Hal ini dilakukan dengan menggunakan setsockopt().

# Mode Promiskuitas (opsional): Jika program berjalan di sistem operasi Windows (os.name == "nt"), maka program akan mengatur mode promiskuitas dengan menggunakan ioctl(). Ini memungkinkan socket untuk menangkap semua paket yang melewati interface, bukan hanya paket yang ditujukan untuk host tersebut.

# Mendengarkan Lalu Lintas: Program memasuki loop utama, dimana akan terus menerima paket-paket jaringan yang datang melalui socket. Paket diterima dengan menggunakan recvfrom(). Hanya 20 byte pertama dari paket yang diambil, yang dianggap sebagai header IP.

# Menguraikan Header IP: Header IP dari paket yang diterima diurai menjadi informasi yang lebih mudah dibaca. Hal ini mencakup alamat IP sumber, alamat IP tujuan, dan protokol yang digunakan.

# Menghentikan Program: Jika pengguna menekan tombol keyboard (Ctrl+C), program akan keluar dari loop. Jika program berjalan di sistem operasi Windows, mode promiskuitas akan dinonaktifkan.

# Program ini berguna untuk tujuan penelitian, analisis keamanan, atau pemantauan jaringan, yang memungkinkan pengguna untuk melihat lalu lintas jaringan yang melewati host mereka.

# ======================================================================================================================================================================================================================================================================================================================== # 
        

# Fungsi:

# Mendengarkan Lalu Lintas Jaringan: Program ini berfungsi untuk menangkap dan mendengarkan lalu lintas jaringan yang melewati host tempat program ini dijalankan. Ini memungkinkan pengguna untuk memantau paket-paket yang dikirim dan diterima oleh host tersebut.

# Menganalisis Header IP: Program ini menganalisis header IP dari paket-paket yang ditangkap, memungkinkan pengguna untuk melihat informasi seperti alamat IP sumber dan tujuan, serta protokol yang digunakan.

# Manfaat:

# Keamanan Jaringan: Program ini dapat digunakan untuk memantau lalu lintas jaringan dan mendeteksi aktivitas yang mencurigakan atau serangan yang sedang terjadi pada jaringan. Ini membantu meningkatkan keamanan jaringan dengan memberikan visibilitas tambahan terhadap aktivitas jaringan yang tidak diinginkan.

# Troubleshooting Jaringan: Dengan memantau lalu lintas jaringan, program ini dapat membantu dalam proses troubleshooting jaringan. Pengguna dapat melihat paket-paket yang dikirim dan diterima oleh host mereka untuk mengidentifikasi masalah atau gangguan jaringan yang mungkin terjadi.

# Penelitian dan Pengembangan: Program ini dapat digunakan oleh peneliti keamanan jaringan dan pengembang perangkat lunak untuk melakukan penelitian lebih lanjut tentang protokol jaringan, analisis serangan jaringan, atau pengembangan alat-alat keamanan jaringan baru.

# Cara Penggunaan:

# Menjalankan Program: Program ini dapat dijalankan di host yang ingin memantau lalu lintas jaringan. Pengguna cukup menjalankan script Python ini pada terminal atau lingkungan pengembangan Python.

# Mengamati Output: Setelah program berjalan, pengguna dapat melihat output yang ditampilkan pada layar terminal. Output ini akan menampilkan informasi tentang paket-paket jaringan yang ditangkap, seperti alamat IP sumber, alamat IP tujuan, dan protokol yang digunakan.

# Pengembangan:

# Peningkatan Fungsionalitas: Program ini dapat dikembangkan dengan menambahkan fungsionalitas tambahan, seperti mendeteksi dan menganalisis paket-paket yang menggunakan protokol khusus, atau menyimpan log dari paket-paket yang ditangkap untuk analisis lebih lanjut.

# Antarmuka Pengguna: Pengembang dapat mengembangkan antarmuka pengguna grafis (GUI) untuk program ini agar lebih mudah digunakan oleh pengguna yang tidak terbiasa dengan baris perintah.

# Optimasi dan Pemeliharaan: Pengembang dapat melakukan optimasi pada kode untuk meningkatkan kinerja program dan memperbaiki bug yang ada. Pemeliharaan rutin juga penting untuk memastikan program tetap berjalan dengan baik di lingkungan yang berubah atau di sistem operasi baru.



