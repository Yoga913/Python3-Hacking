import os
import queue
import threading
import urllib.error
import urllib.parse
import urllib.request

threads = 10
target = "http://www.test.com"
directory = "/Users/justin/Downloads/joomla-3.1.1"
filters = [".jpg", ".gif", "png", ".css"]

os.chdir(directory)
web_paths = queue.Queue()

for r, d, f in os.walk("."):
    for files in f:
        remote_path = "%s/%s" % (r, files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request)
            print("[%d] => %s" % (response.code, path))
            response.close()
        except urllib.error.HTTPError as error:
            print("Failed %s" % error.code)
            pass


for i in range(threads):
    print("Spawning thread: %d" % i)
    t = threading.Thread(target=test_remote)
    t.start()


# =========================================================================== # 
  
# Program ini bertujuan untuk melakukan pengujian keberadaan halaman web atau file-file tertentu dalam sebuah direktori pada sebuah server web. Berikut adalah alur kerja programnya:

# Impor Modul: Program ini mengimpor beberapa modul yang diperlukan seperti os, queue, threading, dan urllib.

# Pengaturan Variabel: Beberapa variabel seperti jumlah thread yang akan digunakan, target URL, direktori yang akan diuji, dan daftar filter untuk jenis file yang akan diabaikan diatur.

# Navigasi ke Direktori: Program berpindah ke direktori yang telah ditentukan di variabel directory menggunakan fungsi os.chdir().

# Membuat Antrian Web Paths: Program membuat antrian (queue) bernama web_paths yang akan berisi path dari file-file yang akan diuji.

# Memenuhi Antrian Web Paths: Program melakukan iterasi melalui setiap file dalam direktori yang ditentukan menggunakan os.walk(). Jika file bukan merupakan file gambar atau file yang tidak termasuk dalam filter yang telah ditentukan, path file tersebut dimasukkan ke dalam antrian web_paths.

# Fungsi test_remote(): Fungsi ini akan dijalankan oleh setiap thread yang dibuat. Fungsi ini bertugas untuk mengambil path dari antrian web_paths, membentuk URL lengkap dengan target, membuat permintaan HTTP menggunakan modul urllib, dan mencetak hasil dari permintaan tersebut.

# Pembuatan Thread: Program kemudian membuat sejumlah thread sesuai dengan jumlah yang telah ditentukan. Setiap thread akan memanggil fungsi test_remote().

# Eksekusi: Setelah semua thread dibuat, program akan mengeksekusi setiap thread yang akan secara bersamaan mengambil path dari antrian web_paths dan melakukan permintaan HTTP ke server target.

# Alur program ini memungkinkan untuk secara paralel melakukan pengujian terhadap berbagai path atau file dalam sebuah direktori di server web, sehingga dapat mempercepat proses pengujian dan memastikan keberadaan file-file yang diinginkan dalam sebuah web.

# =============================================================================================================================================================================================================================================================================================================== # 

# Berikut adalah penjelasan mengenai fungsi, cara penggunaan, dan potensi pengembangan dari program ini:

# Fungsi:

# Pengujian Ketersediaan File: Program ini berfungsi untuk menguji ketersediaan file atau halaman web dalam sebuah direktori di server web yang ditentukan.
# Identifikasi Masalah: Dengan menjalankan program ini, pengguna dapat dengan cepat mengidentifikasi file-file yang mungkin tidak dapat diakses atau tidak ada dalam direktori web yang dituju.
# Automatisasi Pengujian: Program ini memungkinkan untuk melakukan pengujian secara otomatis dengan menggunakan beberapa thread, sehingga mempercepat proses pengujian.

# Cara Penggunaan:

# Pengguna harus menentukan variabel-variabel seperti jumlah thread (threads), URL target (target), direktori yang akan diuji (directory), dan filter jenis file yang akan diabaikan (filters).
# Pastikan direktori yang akan diuji sudah benar-benar ada di server web yang dituju.
# Setelah variabel-variabel sudah diatur, jalankan program untuk memulai pengujian. Program akan secara otomatis mengakses setiap path dalam direktori yang ditentukan dan mencetak hasilnya.

# Pengembangan:

# Antarmuka Pengguna (GUI): Program ini dapat dikembangkan dengan menambahkan antarmuka pengguna grafis (GUI) yang lebih ramah pengguna untuk memudahkan pengaturan variabel dan pemantauan hasil pengujian.
# Peningkatan Efisiensi: Dapat dilakukan peningkatan efisiensi dengan mengoptimalkan penggunaan thread atau dengan menggunakan teknik-teknik lain seperti multiproses.
# Laporan Pengujian yang Lebih Komprehensif: Pengembangan dapat dilakukan dengan menambahkan kemampuan untuk menghasilkan laporan pengujian yang lebih komprehensif, misalnya dengan menyimpan hasil pengujian ke dalam file atau basis data.
# Penanganan Kesalahan yang Lebih Baik: Program dapat diperbaiki dengan menambahkan penanganan kesalahan yang lebih baik untuk menangani situasi seperti koneksi ke server yang gagal atau file yang tidak dapat diakses.
# Penggunaan Filter yang Lebih Fleksibel: Pengguna dapat diberikan kemampuan untuk menentukan filter jenis file yang akan diabaikan secara dinamis, misalnya dengan menggunakan argumen baris perintah atau pengaturan GUI.
# Dengan melakukan pengembangan seperti yang disebutkan di atas, program ini dapat menjadi alat yang lebih kuat dan mudah digunakan untuk pengujian ketersediaan file dalam sebuah server web.

# ========================================================================================================================================================================================================================================================== # 
