import socket
import os
import struct
import threading
from ipaddress import ip_address, ip_network
from ctypes import *

# import library : Program ini menggunakan beberapa modul Python seperti socket, struct, threading, ipaddress, dan ctypes. Modul ini digunakan untuk berbagai tujuan, termasuk bekerja dengan socket, struktur data, dan threading.

# host to listen on
host = "192.168.0.187"

# subnet to target
tgt_subnet = "192.168.0.0/24"

# magic we'll check ICMP responses for
tgt_message = "PYTHONRULES!"

# konfigurasi : Konfigurasi awal mencakup host yang akan mendengarkan, subnet yang akan ditargetkan, dan pesan yang akan digunakan sebagai tanda pengenal.


def udp_sender(sub_net, magic_message): # fungsi udp sender : Fungsi ini digunakan untuk mengirim pesan UDP ke semua host dalam suatu subnet.
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for ip in ip_network(sub_net).hosts():
        sender.sendto(magic_message.encode('utf-8'), (str(ip), 65212))

# fungsi udp sender : Fungsi ini digunakan untuk mengirim pesan UDP ke semua host dalam suatu subnet.

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


class ICMP(Structure):
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
    ]

    def __new__(cls, socket_buffer):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        self.socket_buffer = socket_buffer

# definisi struktur ip dan icmp : Program ini mendefinisikan dua struktur, yaitu IP dan ICMP, yang merepresentasikan format dari header IP dan ICMP. Struktur ini memungkinkan program untuk membaca dan menginterpretasikan data yang diterima dari socket.


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

# inisialisasi socket sniffer: Program membuat sebuah socket raw untuk menangkap paket-paket jaringan. Konfigurasi socket melibatkan pengaturan beberapa opsi, tergantung pada platform (Windows atau non-Windows).

# start sending packets
t = threading.Thread(target=udp_sender, args=(tgt_subnet, tgt_message))
t.start()

# mulai thred pengirim udp : Sebuah thread dibuat untuk mengirim pesan UDP ke host dalam subnet yang ditargetkan.

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
# loop utama :Program memasuki loop utama yang terus membaca paket dari socket, kemudian menginterpretasikan informasi dari header IP dan ICMP, dan mencetak hasilnya.

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
# pengecekan icmp dan host response: Jika paket yang diterima adalah ICMP, program mengambil bagian yang berkaitan dengan header ICMP dan mencetak informasi seperti jenis (type) dan kode (code).


            # now check for the TYPE 3 and CODE 3 which indicates
            # a host is up but no port available to talk to           
            if icmp_header.code == 3 and icmp_header.type == 3:

                # check to make sure we are receiving the response 
                # that lands in our subnet
                if ip_address(ip_header.src_address) in ip_network(tgt_subnet):

                    # test for our magic message
                    if raw_buffer[len(raw_buffer)
                       - len(tgt_message):] == tgt_message:
                        print("Host Up: %s" % ip_header.src_address)
# pengecekan host up dan magic massage: Program melakukan pengecekan khusus untuk paket ICMP dengan tipe 3 dan kode 3, yang menunjukkan bahwa host berada dalam kondisi UP tetapi tidak ada port yang tersedia untuk berkomunikasi. Jika host tersebut berada dalam subnet yang ditargetkan dan memiliki pesan yang sesuai, maka host tersebut dianggap "Up".

# handle CTRL-C
except KeyboardInterrupt:
    # if we're on Windows turn off promiscuous mode
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

# penanganan keyboard interrupt : Program menangani penekanan tombol Ctrl-C dengan membersihkan pengaturan socket promiskuitas jika aplikasi dijalankan di lingkungan Windows.

# ======================================================================================================================================================================== # 
# Program ini adalah sebuah sniffer sederhana yang dirancang untuk mendeteksi host dalam suatu subnet yang merespon ke sebuah pesan khusus dalam protokol ICMP.

# Program ini memanfaatkan teknik-sniffing sederhana untuk mendeteksi host dalam subnet yang merespon pesan khusus melalui protokol ICMP. Dengan menggunakan wawasan ini, Anda dapat memahami alur kerja dan logika di balik program tersebut.