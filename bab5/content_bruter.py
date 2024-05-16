import queue
import threading
import urllib.error
import urllib.parse
import urllib.request

threads = 50
target_url = "http://testphp.vulnweb.com"
wordlist_file = "all.txt"  # from SVNDigger
resume = None
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) " \
             "Gecko/20100101 " \
             "Firefox/19.0"


def build_wordlist(wordlst_file):
    # read in the word list
    fd = open(wordlst_file, "r")
    raw_words = [line.rstrip('\n') for line in fd]
    fd.close()

    found_resume = False
    words = queue.Queue()

    for word in raw_words:
        if resume:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: %s" % resume)
        else:
            words.put(word)
    return words


def dir_bruter(extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []

        # check if there is a file extension if not
        # it's a directory path we're bruting
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)

        # if we want to bruteforce extensions
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt, extension))

        # iterate over our list of attempts        
        for brute in attempt_list:
            url = "%s%s" % (target_url, urllib.parse.quote(brute))
            try:
                headers = {"User-Agent": user_agent}
                r = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(r)
                if len(response.read()):
                    print("[%d] => %s" % (response.code, url))
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    print("!!! %d => %s" % (e.code, url))
                pass


word_queue = build_wordlist(wordlist_file)
file_extensions = [".php", ".bak", ".orig", ".inc"]

for i in range(threads):
    t = threading.Thread(target=dir_bruter, args=(file_extensions,))
    t.start()

# ================================================================================ # 
    
# Program Python ini merupakan implementasi dari alat yang digunakan untuk melakukan serangan bruteforce terhadap direktori dan file pada suatu website. Berikut adalah penjelasan alur programnya:

# Impor modul yang diperlukan:

# queue: Modul ini digunakan untuk mengimplementasikan antrian.
# threading: Digunakan untuk membuat dan mengelola threading.
# urllib.error, urllib.parse, urllib.request: Modul ini digunakan untuk melakukan HTTP request.
# Tentukan parameter dan konfigurasi:

# threads: Jumlah thread yang akan digunakan untuk melakukan bruteforce.
# target_url: URL target yang akan diserang.
# wordlist_file: Nama file yang berisi daftar kata-kata yang akan digunakan dalam serangan.
# resume: Jika ada, digunakan untuk melanjutkan serangan dari kata tertentu dalam daftar.
# user_agent: User agent yang akan digunakan dalam setiap permintaan HTTP.

# Buat fungsi build_wordlist:

# Fungsi ini membaca daftar kata-kata dari file wordlist yang telah ditentukan.
# Jika ada parameter resume, fungsi ini akan mulai membaca daftar kata-kata dari kata tersebut.
# Fungsi ini mengembalikan antrian (Queue) yang berisi kata-kata yang akan digunakan dalam serangan.

# Buat fungsi dir_bruter:

# Fungsi ini berisi logika utama serangan bruteforce terhadap direktori dan file.
# Fungsi ini akan mengambil kata dari antrian kata-kata yang belum diproses.
# Setiap kata yang diambil akan dibuat menjadi daftar percobaan (attempt_list) yang mungkin berupa direktori atau file dengan ekstensi tertentu.
# Kemudian, fungsi akan mencoba mengakses URL yang disusun dari target URL dan percobaan yang dibuat.
# Jika respons dari server tidak kosong, akan dicetak kode respons HTTP dan URL.
# Jika terjadi kesalahan HTTP selain 404 (Not Found), akan dicetak pesan kesalahan.
# Buat antrian kata-kata (word_queue) dengan memanggil fungsi build_wordlist.

# Tentukan ekstensi file yang akan dicoba (file_extensions).

# Loop untuk membuat dan menjalankan thread sebanyak yang ditentukan dalam threads:

# Setiap thread akan memanggil fungsi dir_bruter dengan argumen file_extensions.
# Thread-thread tersebut akan berjalan secara konkuren untuk melakukan serangan bruteforce.
# Program ini bekerja dengan menggunakan beberapa thread untuk secara bersamaan melakukan bruteforce terhadap berbagai direktori dan file yang mungkin ada di dalam website target.


# =============================================================================================================================================================================================== # 
    
# Fungsi build_wordlist:
# Manfaat:
# Fungsi ini digunakan untuk membaca daftar kata-kata dari sebuah file wordlist yang kemudian akan digunakan dalam serangan bruteforce.
# Memungkinkan untuk melanjutkan serangan dari kata tertentu jika parameter resume diberikan.

# Cara Penggunaan:
# Panggil fungsi build_wordlist dengan menyertakan nama file wordlist sebagai argumen.
# Fungsi akan membaca file wordlist dan memuat kata-kata ke dalam antrian (queue).
# Jika ingin melanjutkan serangan dari kata tertentu, tentukan nilai parameter resume dengan kata tersebut.


# Pengembangan:
# Untuk pengembangan, dapat ditambahkan fitur seperti:
# Validasi dan pemrosesan kata-kata dalam wordlist untuk memastikan konsistensi.
# Kemampuan untuk memfilter atau memanipulasi kata-kata berdasarkan kriteria tertentu.
# Integrasi dengan sumber kata-kata eksternal, misalnya API untuk memperoleh wordlist dari berbagai sumber.

# Fungsi dir_bruter:

# Manfaat:
# Fungsi ini merupakan inti dari serangan bruteforce terhadap direktori dan file di dalam website target.
# Membuat percobaan URL berdasarkan kata-kata dalam wordlist dan ekstensi file yang ditentukan.
# Mengirim permintaan HTTP ke URL yang dibuat untuk menentukan apakah direktori atau file ada atau tidak.

# Cara Penggunaan:
# Panggil fungsi dir_bruter.
# Pastikan wordlist telah dibuat dan dimuat ke dalam antrian.
# Tentukan ekstensi file yang ingin di-bruteforce, jika diperlukan.
# Fungsi akan secara iteratif mengambil kata-kata dari antrian dan mencoba untuk mengakses URL yang dibuat dari kata tersebut.
# Hasil serangan akan ditampilkan di konsol.

# Pengembangan:

# Untuk pengembangan, dapat ditambahkan fitur seperti:
# Penanganan lebih lanjut terhadap respons HTTP yang diterima, seperti penanganan kode respons khusus.
# Pengaturan yang lebih fleksibel untuk user agent, header, atau parameter HTTP lainnya.
# Kemampuan untuk melakukan serangan dengan menggunakan teknik lain selain bruteforce, seperti fuzzing atau scanning.

# Penggunaan dan Pengembangan Umum:

# Manfaat:
# Program ini dapat digunakan untuk melakukan serangan bruteforce terhadap website yang memungkinkan akses terhadap direktori dan file.
# Dapat digunakan untuk menguji keamanan suatu website dengan mencoba menemukan direktori atau file yang mungkin tersembunyi atau tidak diinginkan.

# Cara Penggunaan:
# Atur konfigurasi yang diperlukan seperti jumlah thread, URL target, dan file wordlist.
# Jalankan program Python dengan mengatur parameter-parameter yang sesuai.
# Perhatikan hasil serangan yang ditampilkan di konsol.

# Pengembangan:
# Untuk pengembangan, dapat dilakukan peningkatan fitur seperti:
# Penggunaan teknik serangan yang lebih canggih atau spesifik.
# Penambahan modul atau fungsionalitas tambahan untuk meningkatkan fleksibilitas dan efisiensi serangan.
# Integrasi dengan alat-alat atau layanan keamanan lainnya untuk analisis lebih lanjut terhadap hasil serangan.



