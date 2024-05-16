import socket
import os
import struct

from ctypes import *

# host to listen on
host = "192.168.0.187"


class IP(Structure):
    
    _fields_ = [
        ("ihl",           c_ubyte, 4),
        ("version",       c_ubyte, 4),
        ("tos",           c_ubyte),
        ("len",           c_ushort),
        ("id",            c_ushort),
        ("offset",        c_ushort),
        ("ttl",           c_ubyte),
        ("protocol_num",  c_ubyte),
        ("sum",           c_ushort),
        ("src",           c_uint32),
        ("dst",           c_uint32)
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


class ICMP(Structure):
    
    _fields_ = [
        ("type",         c_ubyte),
        ("code",         c_ubyte),
        ("checksum",     c_ushort),
        ("unused",       c_ushort),
        ("next_hop_mtu", c_ushort)
        ]
    
    def __new__(cls, socket_buffer):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        self.socket_buffer = socket_buffer


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

        # if it's ICMP we want it
        if ip_header.protocol == "ICMP":
            # calculate where our ICMP packet starts
            offset = ip_header.ihl * 4
            buf = raw_buffer[offset:offset + sizeof(ICMP)]
            
            # create our ICMP structure
            icmp_header = ICMP(buf)
            
            print("ICMP -> Type: %d Code: %d" % (
                icmp_header.type,
                icmp_header.code)
                  )

# handle CTRL-C
except KeyboardInterrupt:
    # if we're on Windows turn off promiscuous mode
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

# =========================================================================== # 
        
# Program tersebut merupakan sebuah sniffer sederhana yang digunakan untuk menangkap dan menganalisis paket-paket jaringan yang melewati host yang menjalankan program tersebut. Berikut adalah alur kerjanya:

# 1. **Inisialisasi Variabel dan Struktur Data**: 
#     - Variabel `host` menentukan alamat IP host tempat program dijalankan.
#     - Terdapat dua struktur data, yaitu `IP` dan `ICMP`, yang direpresentasikan sebagai kelas dengan menggunakan modul `ctypes`. Struktur data ini mewakili header IP dan header ICMP pada paket-paket jaringan.

# 2. **Membuat Socket**: Program membuat sebuah socket raw menggunakan modul `socket`. Socket ini akan digunakan untuk menangkap paket-paket jaringan.

# 3. **Mengikat Socket**: Socket diikat ke alamat host dan port 0, sehingga socket akan menangkap semua paket yang tiba pada host tersebut.

# 4. **Mengatur Opsi Socket**: Opsi socket diatur agar header IP disertakan dalam data yang diterima, sehingga program dapat membaca header IP dari paket-paket yang ditangkap.

# 5. **Mode Promiskuitas (opsional)**: Jika program dijalankan di sistem operasi Windows (`os.name == "nt"`), maka program akan mengatur mode promiskuitas untuk socket. Hal ini memungkinkan socket untuk menangkap semua paket yang melewati interface, bukan hanya paket yang ditujukan untuk host tersebut.

# 6. **Loop Utama**: Program memasuki sebuah loop utama yang akan terus berjalan hingga program dihentikan.
#     - Program membaca satu paket jaringan pada setiap iterasi loop menggunakan `recvfrom()`.
#     - Dari paket yang diterima, program mengambil 20 byte pertama untuk membuat objek `IP` yang mewakili header IP dari paket tersebut.
#     - Program mencetak informasi tentang header IP yang baru saja dibuat, seperti protokol yang digunakan, alamat IP sumber, dan alamat IP tujuan.
#     - Jika protokol yang digunakan adalah ICMP, program akan mengambil bagian yang tepat dari paket untuk membuat objek `ICMP`. Objek ini kemudian digunakan untuk mencetak informasi tentang header ICMP, seperti tipe dan kode.

# 7. **Penanganan KeyboardInterrupt**: Jika pengguna menekan tombol keyboard (Ctrl+C), program akan keluar dari loop. Jika program dijalankan di sistem operasi Windows, mode promiskuitas akan dinonaktifkan.
        
# ========================================================================================================================================================================================================================================================================================================================= # 
        
# Manfaat:

# Mendeteksi Masalah Jaringan: Program ini dapat digunakan untuk mendeteksi masalah jaringan dengan menganalisis paket-paket yang melewati host. Misalnya, program ini dapat membantu dalam mengidentifikasi paket-paket yang hilang, terfragmentasi, atau terganggu.

# Menganalisis Serangan Jaringan: Dengan program ini, pengguna dapat menganalisis paket-paket jaringan untuk mendeteksi serangan jaringan seperti serangan Denial-of-Service (DoS) atau serangan brute force. Hal ini membantu dalam meningkatkan keamanan jaringan dengan memungkinkan deteksi dini terhadap serangan yang sedang terjadi.

# Monitoring Jaringan: Program ini dapat digunakan sebagai alat monitoring jaringan untuk melihat lalu lintas jaringan yang melewati host, dan memantau kinerja jaringan secara keseluruhan.

# Cara Penggunaan:

# Menjalankan Program: Program ini dapat dijalankan di host yang ingin memantau lalu lintas jaringan. Pengguna cukup menjalankan script Python ini pada terminal atau lingkungan pengembangan Python.

# Melihat Output: Setelah program berjalan, pengguna dapat melihat output yang ditampilkan pada layar terminal. Output ini akan menampilkan informasi tentang paket-paket jaringan yang ditangkap, seperti alamat IP sumber, alamat IP tujuan, protokol yang digunakan, serta informasi tambahan jika protokol yang digunakan adalah ICMP.

# Pengembangan:

# Peningkatan Analisis: Program ini dapat dikembangkan dengan menambahkan analisis tambahan untuk protokol lain selain ICMP. Misalnya, pengembang dapat menambahkan fitur untuk menganalisis protokol TCP atau UDP.

# Penyimpanan Data: Pengembang dapat menambahkan fungsionalitas untuk menyimpan log dari paket-paket jaringan yang ditangkap ke dalam database atau file untuk analisis lebih lanjut atau pemantauan jangka panjang.

# Antarmuka Pengguna: Program ini dapat dikembangkan dengan menambahkan antarmuka pengguna grafis (GUI) agar lebih mudah digunakan oleh pengguna yang tidak terbiasa dengan baris perintah.

# Optimasi dan Pemeliharaan: Pengembang dapat melakukan optimasi pada kode untuk meningkatkan kinerja program dan memperbaiki bug yang ada. Pemeliharaan rutin juga penting untuk memastikan program tetap berjalan dengan baik di lingkungan yang berubah atau di sistem operasi baru.

# ====================================================================================================================================================================================================================================================================================================================================================== # 