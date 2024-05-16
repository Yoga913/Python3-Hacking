from kamene.all import *


# our packet callback
def packet_callback(packet):
    if packet[TCP].payload:
        mail_packet = bytes(packet[TCP].payload)
        if b'user' in mail_packet.lower() or b'pass' in mail_packet.lower():
            print("[*] Server: %s" % packet[IP].dst)
            print("[*] %s" % packet[TCP].payload)


# fire up our sniffer
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143",
      prn=packet_callback,
      store=0)


# ======================================================================================= # 

# Program tersebut menggunakan library Kamene (sebelumnya dikenal sebagai Scapy) untuk menangkap dan memeriksa paket-paket jaringan. Berikut adalah alur kerjanya:

# Import Library: Program mengimpor semua fungsi dan kelas yang diperlukan dari library Kamene menggunakan pernyataan from kamene.all import *. Kamene adalah sebuah library Python yang powerful untuk memanipulasi paket jaringan secara mudah dan fleksibel.

# Definisi Fungsi packet_callback:

# Fungsi ini bertindak sebagai callback yang akan dipanggil setiap kali paket jaringan diterima oleh sniffer.
# Parameter packet mewakili paket jaringan yang diterima.
# Dalam fungsi ini, program memeriksa apakah paket tersebut merupakan paket TCP yang memiliki payload (data).
# Jika paket TCP tersebut mengandung string "user" atau "pass" (kata kunci yang mungkin terkait dengan pengiriman nama pengguna atau kata sandi), maka program akan mencetak alamat IP tujuan (packet[IP].dst) serta payload dari paket tersebut (packet[TCP].payload).
# Memulai Sniffer: Program memulai sniffer menggunakan fungsi sniff() dari library Kamene:

# Parameter filter digunakan untuk menentukan filter berdasarkan protokol dan port. Dalam hal ini, program menetapkan filter untuk hanya menangkap paket-paket TCP yang menuju ke port 110 (POP3), port 25 (SMTP), atau port 143 (IMAP).
# Parameter prn menentukan fungsi callback yang akan dipanggil setiap kali paket diterima oleh sniffer. Dalam hal ini, fungsi packet_callback digunakan sebagai callback.
# Parameter store digunakan untuk menentukan apakah paket yang ditangkap akan disimpan di memori atau tidak. Dalam hal ini, nilai 0 menunjukkan bahwa paket tidak akan disimpan.
# Dengan cara ini, program akan berjalan sebagai sniffer yang akan memeriksa setiap paket jaringan yang melewati port 110, 25, atau 143. Jika paket tersebut mengandung kata kunci "user" atau "pass", maka program akan mencetak informasi tentang paket tersebut, termasuk alamat IP tujuan dan payload-nya. Hal ini dapat digunakan untuk mendeteksi potensial kiriman nama pengguna dan kata sandi yang dikirimkan secara tidak aman melalui protokol email.

# ============================================================================================================================================================================================================================================================================================================================================================================================================================================================================ # 

# Fungsi:
# Memeriksa Paket Jaringan: Program ini memiliki fungsi untuk memeriksa paket-paket jaringan yang melewati port-port tertentu (port 110, 25, dan 143) menggunakan library Kamene.

# Pencarian Kata Kunci Sensitif: Program akan mencari kata kunci sensitif seperti "user" atau "pass" di dalam payload dari paket-paket TCP yang ditangkap. Ini membantu dalam mendeteksi potensial kiriman nama pengguna dan kata sandi yang dikirimkan secara tidak aman.

# Manfaat:
# Keamanan Jaringan: Program ini membantu meningkatkan keamanan jaringan dengan memberikan kemampuan untuk mendeteksi potensial kiriman informasi sensitif seperti nama pengguna dan kata sandi yang dikirimkan melalui protokol email dengan cara yang tidak aman.

# Deteksi Serangan: Program ini dapat membantu dalam mendeteksi serangan atau aktivitas mencurigakan yang terkait dengan upaya pencurian kredensial melalui jaringan.

# Cara Penggunaan:
# Menjalankan Program: Pengguna menjalankan program ini di lingkungan Python.

# Memantau Output: Selama program berjalan, pengguna dapat melihat output yang mencakup alamat IP tujuan dari paket-paket yang memuat kata kunci sensitif, serta payload dari paket tersebut.

# Pengembangan:
# Peningkatan Fungsionalitas: Program ini dapat ditingkatkan dengan menambahkan fitur-fitur tambahan seperti deteksi lebih banyak kata kunci sensitif, mendukung protokol lain selain TCP, atau mencatat semua paket yang mengandung kata kunci sensitif ke dalam sebuah file log.

# Optimasi Performa: Pengembang dapat melakukan optimasi pada kode untuk meningkatkan kinerja program, seperti dengan mengurangi beban pemrosesan data atau mempercepat pencarian kata kunci sensitif.

# Pemantauan Aktivitas Jaringan: Program ini juga dapat dikembangkan menjadi alat pemantauan aktivitas jaringan yang lebih kompleks, misalnya dengan menambahkan kemampuan untuk melacak dan menganalisis pola lalu lintas jaringan yang mencurigakan.

# ======================================================================================================================================================================================================================================================================================================== # 



