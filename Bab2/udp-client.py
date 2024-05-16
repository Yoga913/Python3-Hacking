import socket

target_host = "127.0.0.1"
target_port = 80

# inisialisasi target : Program menetapkan alamat dan port tujuan yang akan digunakan untuk mengirim dan menerima data.

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# membuat objeck socket : Program membuat objek socket menggunakan modul socket. Jenis socket yang digunakan adalah SOCK_DGRAM untuk koneksi UDP.

# send some data
client.sendto(b"AAABBBCCC", (target_host, target_port))

# mengirim data : Klien mengirim data ke alamat dan port tujuan menggunakan metode sendto. Pada contoh ini, klien mengirimkan data berupa string byte "AAABBBCCC".

# receive some data
data, addr = client.recvfrom(4096)

# menerima data : Klien menerima data dari server menggunakan metode recvfrom. Panjang maksimal data yang akan diterima adalah 4096 byte. Metode recvfrom mengembalikan data dan alamat sumber data.

client.close()

# menutup koneksi : Setelah proses pengiriman dan penerimaan data selesai, klien menutup socket dengan metode close.

print(data)

# mencetak data yang di terima : Program mencetak data yang diterima dari server.

# =================================================================================================================================================== # 
# Program Python di atas adalah contoh penggunaan UDP (User Datagram Protocol) untuk mengirim dan menerima data antara klien dan server. 


# Manfaat:
# Program ini mengilustrasikan penggunaan UDP untuk komunikasi antara klien dan server. Manfaatnya antara lain:
# Berguna untuk aplikasi yang memerlukan komunikasi yang lebih cepat dan ringan daripada TCP, seperti permainan online atau aliran video.
# Cocok untuk situasi di mana keterlambatan tidak terlalu kritis dan ada toleransi terhadap kehilangan paket.

# Cara Penggunaan:
# Tetapkan nilai target_host dan target_port sesuai dengan alamat dan port server tujuan.

# Jalankan program untuk mengirimkan data ke server dan menerima respons dari server.

# Pengembangan Potensial:
# Program ini dapat dikembangkan lebih lanjut dengan menambahkan fitur-fitur berikut:

# Error Handling: Menambahkan mekanisme penanganan kesalahan untuk situasi di mana koneksi atau pengiriman data tidak berhasil.
# Pengiriman Data yang Lebih Kompleks: Mengirimkan dan menerima data yang lebih kompleks seperti objek JSON atau pesan terstruktur lainnya.
# Multithreading atau Multiprocessing: Mengimplementasikan multithreading atau multiprocessing untuk menangani koneksi dari beberapa klien secara bersamaan.
# Keamanan: Jika diperlukan, tambahkan lapisan keamanan seperti enkripsi untuk melindungi data yang dikirim dan diterima.
# Logging: Menambahkan sistem logging untuk melacak aktivitas dan pemecahan masalah.



