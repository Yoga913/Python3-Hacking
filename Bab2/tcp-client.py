import socket

target_host = "www.google.com"
target_port = 80

# inisialisasi variabel target : Program menentukan tujuan koneksi dengan menentukan alamat tujuan (target_host) dan port tujuan (target_port). Pada contoh ini, tujuan koneksi adalah server web Google pada port 80.

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# membuat obleck socket : Program membuat objek socket menggunakan modul socket. Jenis socket yang digunakan adalah SOCK_STREAM yang mengindikasikan bahwa koneksi adalah koneksi TCP.

# connect the client
client.connect((target_host, target_port))

# menghubungkan klien ke server : Klien terhubung ke server web dengan menggunakan metode connect dan menyertakan tuple berisi alamat target dan port target.

# send some data
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# mengimport data : Klien mengirimkan data ke server menggunakan metode send. Dalam hal ini, klien mengirimkan permintaan HTTP GET untuk halaman utama Google.

# receive data
response = client.recv(4096)

# menerima data : Klien menerima data dari server menggunakan metode recv. Panjang maksimal data yang akan diterima adalah 4096 byte.

client.close()

# menutup koneksi : Setelah koneksi selesai, klien menutup socket dengan metode close.

print(response)

# mencetak respon : Program mencetak respons yang diterima dari server, dalam hal ini, respons dari permintaan HTTP GET yang dikirim.

# =============================================================================================================================================# 
# Program Python di atas menggunakan modul socket untuk membuat koneksi ke server web (dalam hal ini, Google) dan mengirim permintaan HTTP. 

# Manfaat:
# Program ini dapat digunakan untuk membuat koneksi TCP sederhana ke server web dan mengirimkan permintaan HTTP. Hal ini berguna untuk membuat koneksi ke server dan berkomunikasi dengan protokol tertentu, seperti protokol web HTTP.

# Cara Penggunaan:
# Ganti nilai target_host dengan alamat server yang ingin Anda hubungi.
# Sesuaikan nilai target_port sesuai dengan port target yang diinginkan (misalnya, port 80 untuk HTTP).
# Jalankan program Python tersebut untuk membuat koneksi ke server dan mendapatkan respons dari permintaan HTTP yang dikirimkan.



