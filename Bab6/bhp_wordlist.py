#!/usr/bin/env python
# -*- coding: utf-8 -*-
from burp import IBurpExtender
from burp import IContextMenuFactory
from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL
import re
from datetime import datetime
from html.parser import HTMLParser


class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []

    def handle_data(self, data):
        self.page_text.append(data)

    def handle_comment(self, data):
        self.handle_data(data)

    def strip(self, html):
        self.feed(html)
        return " ".join(self.page_text)


class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()

        # start with something we know is common
        self.wordlist = {"password"}

        # we set up our extension
        callbacks.setExtensionName("BHP Wordlist")
        callbacks.registerContextMenuFactory(self)
        return

    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Create Wordlist",
                                actionPerformed=self.wordlist_menu))
        return menu_list

    def wordlist_menu(self, event):
        # grab the details of what the user clicked
        http_traffic = self.context.getSelectedMessages()

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            self.hosts.add(host)
            http_response = traffic.getResponse()
            if http_response:
                self.get_words(http_response)
        self.display_wordlist()
        return

    def get_words(self, http_response):
        headers, body = http_response.tostring().split('\r\n\r\n', 1)

        # skip non-text responses
        if headers.lower().find("content-type: text") == -1:
            return

        tag_stripper = TagStripper()
        page_text = tag_stripper.strip(body)
        words = re.findall(r'[a-zA-Z]\w{2,}', page_text)

        for word in words:
            # filter out long strings
            if len(word) <= 12:
                self.wordlist.add(word.lower())
        return

    @staticmethod
    def mangle(word):
        year = datetime.now().year
        suffixes = ["", "1", "!", year]
        mangled = []
        for password in (word, word.capitalize()):
            for suffix in suffixes:
                mangled.append("%s%s" % (password, suffix))
        return mangled

    def display_wordlist(self):
        print("# BHP Wordlist for site(s) %s" % ", ".join(self.hosts))
        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)
        return


# =====================================================================================# 
    
# Program tersebut merupakan sebuah ekstensi untuk Burp Suite yang bertujuan untuk membuat daftar kata (wordlist) yang potensial dari lalu lintas HTTP yang ditangkap. Berikut adalah penjelasan alur programnya:

# 1. **Import Library**: Program mengimpor beberapa kelas yang diperlukan dari pustaka Burp, Java, serta beberapa modul Python seperti `re`, `datetime`, dan `html.parser`.

# 2. **TagStripper Class**: Ini adalah subclass dari `HTMLParser` yang bertujuan untuk menghilangkan tag HTML dari teks halaman web. Metode `handle_data` dan `handle_comment` digunakan untuk menangani data dan komentar dalam HTML, sementara metode `strip` digunakan untuk menghilangkan tag HTML dari teks halaman.

# 3. **BurpExtender Class**: Kelas utama yang mengimplementasikan `IBurpExtender` dan `IContextMenuFactory`.

#     - `registerExtenderCallbacks`: Metode ini dipanggil oleh Burp saat ekstensi dimuat. Di dalamnya, ekstensi mendaftarkan dirinya sebagai factory untuk menciptakan menu konteks.
    
#     - `createMenuItems`: Metode ini menciptakan item-menu untuk menu konteks. Item-menu yang diciptakan adalah "Create Wordlist" yang akan memicu metode `wordlist_menu` saat di-klik.
    
#     - `wordlist_menu`: Metode ini dipanggil saat pengguna mengklik item-menu "Create Wordlist". Metode ini menangani pembuatan wordlist dengan memeriksa lalu lintas HTTP yang dipilih oleh pengguna, mengekstrak teks dari respon HTTP, dan memanggil metode `get_words` untuk mendapatkan kata-kata dari teks tersebut. Setelah selesai, metode ini memanggil `display_wordlist` untuk menampilkan wordlist yang telah dibuat.
    
#     - `get_words`: Metode ini menerima respon HTTP, mengekstrak teks darinya, dan menggunakan ekspresi reguler untuk menemukan kata-kata dari teks tersebut. Kata-kata yang ditemukan kemudian dimasukkan ke dalam wordlist, dengan memanggil metode `mangle` untuk menghasilkan variasi kata-kata.
    
#     - `mangle`: Metode ini menerima sebuah kata dan mengembalikan daftar variasi dari kata tersebut. Variasi kata-kata ini mencakup kata itu sendiri, kata dengan huruf pertama kapital, serta tambahan sufiks seperti angka 1, tanda seru, dan tahun sekarang.
    
#     - `display_wordlist`: Metode ini bertanggung jawab untuk menampilkan wordlist yang telah dibuat ke konsol. Wordlist akan ditampilkan bersama dengan host dari lalu lintas HTTP yang telah dianalisis.

# Program ini berguna bagi peneliti keamanan untuk mengumpulkan kata-kata yang mungkin digunakan dalam serangan pencarian kata sandi atau serangan brute force pada aplikasi web yang dituju. Wordlist ini kemudian dapat digunakan untuk menguji kekuatan kata sandi atau mengidentifikasi celah keamanan dalam aplikasi web tersebut.

# ============================================================================================================================================================================================================================================================================================================================================================================ # 
    
# Fungsi:
# Membuat Wordlist Otomatis: Program ini berfungsi untuk membuat wordlist secara otomatis dari lalu lintas HTTP yang ditangkap oleh Burp Suite. Wordlist ini berisi kata-kata yang diekstrak dari teks halaman web yang ditemukan dalam respon HTTP.

# Mangling Kata-kata: Program juga melakukan proses "mangling" terhadap kata-kata yang diekstrak, yaitu menghasilkan variasi kata-kata dengan menambahkan sufiks seperti angka, tanda seru, dan tahun saat ini. Ini memperluas cakupan wordlist dan meningkatkan kemungkinan mencocokkan kata sandi dalam serangan pencarian kata sandi.

# Pengelompokkan Berdasarkan Host: Program dapat mengelompokkan kata-kata yang diekstrak berdasarkan host dari lalu lintas HTTP. Ini memungkinkan pengguna untuk memahami wordlist yang dibuat untuk setiap situs web yang dituju, memfasilitasi pengujian terfokus pada setiap aplikasi web secara terpisah.

# Manfaat:
# Pengujian Keamanan Aplikasi Web: Program ini sangat berguna bagi para profesional keamanan untuk mengumpulkan kata-kata yang mungkin digunakan dalam serangan pencarian kata sandi atau serangan brute force pada aplikasi web yang dituju. Dengan wordlist yang dihasilkan, mereka dapat menguji kekuatan kata sandi atau mencari celah keamanan dalam aplikasi web tersebut.

# Automatisasi Proses: Program ini otomatis mengumpulkan kata-kata dari lalu lintas HTTP yang ditangkap oleh Burp Suite, mengurangi waktu dan upaya yang diperlukan untuk membuat wordlist secara manual. Hal ini memungkinkan para profesional keamanan untuk fokus pada analisis hasil pengujian dan tindakan lanjut yang diperlukan.

# Penggunaan:
# Instalasi Ekstensi: Pengguna harus menginstal ekstensi ini ke dalam Burp Suite, dan kemudian mengaktifkannya.

# Pemilihan Respon HTTP: Pengguna dapat memilih lalu lintas HTTP yang ingin dijadikan basis untuk pembuatan wordlist. Ini bisa dilakukan dengan memilih pesan-pesan HTTP yang terlihat di Proyek Repeater atau Intruder di Burp Suite.

# Membuat Wordlist: Pengguna kemudian harus memilih opsi "Create Wordlist" dari menu konteks yang muncul. Ini akan memicu program untuk mengekstrak kata-kata dari teks halaman web dalam respon HTTP yang dipilih dan menyusunnya menjadi wordlist.

# Menampilkan Wordlist: Setelah wordlist dibuat, program akan menampilkan wordlist tersebut di konsol Burp Suite. Pengguna dapat menggunakan wordlist ini untuk tujuan pengujian keamanan atau penyelidikan lebih lanjut.

# Pengembangan:
# Peningkatan Algoritma Ekstraksi: Pengembangan program ini dapat melibatkan peningkatan algoritma untuk ekstraksi kata-kata dari teks halaman web. Ini dapat meningkatkan akurasi dan efisiensi dalam pembuatan wordlist.

# Penambahan Fungsionalitas: Pengembangan program bisa berfokus pada penambahan fungsionalitas tambahan, seperti dukungan untuk ekstraksi kata-kata dari sumber daya non-teks, atau integrasi dengan alat-alat keamanan lainnya.

# Antarmuka Pengguna: Pengembangan bisa mencakup pengembangan antarmuka pengguna yang lebih ramah pengguna untuk menampilkan dan mengelola wordlist, serta memberikan opsi konfigurasi tambahan.

# Optimisasi Kinerja: Pengembangan juga bisa fokus pada optimisasi kinerja program, seperti mengurangi beban komputasi atau mempercepat proses pembuatan wordlist.

# Dengan melakukan pengembangan yang sesuai, program ini dapat menjadi alat yang lebih kuat dan efektif bagi para profesional keamanan untuk menguji keamanan aplikasi web secara lebih menyeluruh.




