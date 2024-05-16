import base64
import json
import re
import socket
import urllib.error
import urllib.parse
import urllib.request

from burp import IBurpExtender
from burp import IContextMenuFactory
from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem

bing_api_key = "YOURKEYHERE"


class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None

        # we set up our extension
        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContextMenuFactory(self)
        return

    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Send to Bing", actionPerformed=self.bing_menu))
        return menu_list

    def bing_menu(self, event):
        # grab the details of what the user clicked
        http_traffic = self.context.getSelectedMessages()
        print("%d requests highlighted" % len(http_traffic))

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            print("User selected host: %s" % host)
            self.bing_search(host)
        return

    def bing_search(self, host):

        # check if we have an IP or hostname
        is_ip = re.match(r'[0-9]+(?:\.[0-9]+){3}', host)

        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True

        bing_query_string = "'ip:%s'" % ip_address
        self.bing_query(bing_query_string)

        if domain:
            bing_query_string = "'domain:%s'" % host
            self.bing_query(bing_query_string)

    def bing_query(self, bing_query_string):

        print("Performing Bing search: %s" % bing_query_string)

        # encode our query
        quoted_query = urllib.parse.quote(bing_query_string)

        http_request = "GET https://api.datamarket.azure.com/Bing/Search/Web?$format=json&$top=20&Query=%s HTTP/1.1\r\n" % quoted_query
        http_request += "Host: api.datamarket.azure.com\r\n"
        http_request += "Connection: close\r\n"
        http_request += "Authorization: Basic %s\r\n" % base64.b64encode(
            ":%s" % bing_api_key)
        http_request += "User-Agent: Blackhat Python\r\n\r\n"

        json_body = self._callbacks.makeHttpRequest("api.datamarket.azure.com",
                                                    443, True,
                                                    http_request).tostring()

        json_body = json_body.split("\r\n\r\n", 1)[1]

        try:
            r = json.loads(json_body)
            if len(r["d"]["results"]):
                for site in r["d"]["results"]:
                    print("*" * 100)
                    print(site['Title'])
                    print(site['Url'])
                    print(site['Description'])
                    print("*" * 100)
                    j_url = URL(site['Url'])
                    if not self._callbacks.isInScope(j_url):
                        print("Adding to Burp scope")
                        self._callbacks.includeInScope(j_url)
        except:
            print("No results from Bing")
            pass
        return


# ========================================================================= # 
# ini adalah ekstansi burp suite yang memungkin penggunak untuk melakukan pencarian menggunakan layanan bing terhadap host atau ip yang dipiling melalui lalulintas http yang ditangkap melalui burp suite : 
    
# Berikut adalah alur kerja program tersebut:

# Impor Modul dan Pendefinisian Variabel Global:

# Program dimulai dengan mengimpor modul-modul yang diperlukan seperti base64, json, re, socket, dan urllib.
# Variabel global bing_api_key didefinisikan. Anda harus mengganti YOURKEYHERE dengan kunci API Bing yang valid.

# Definisi Kelas BurpExtender:

# Kelas BurpExtender diimplementasikan dengan mewarisi antarmuka IBurpExtender dan IContextMenuFactory.
# Metode registerExtenderCallbacks digunakan untuk mendaftarkan ekstensi dan mengatur nama serta menu konteks.
# Metode createMenuItems digunakan untuk membuat item menu yang akan ditambahkan ke konteks.
# Metode bing_menu dipanggil ketika item menu "Send to Bing" dipilih oleh pengguna.

# Pencarian Bing:

# Metode bing_search digunakan untuk menentukan apakah input adalah alamat IP atau nama host, kemudian melakukan pencarian Bing berdasarkan alamat IP atau nama host tersebut.
# Metode bing_query digunakan untuk membuat permintaan HTTP ke API Bing dengan mengirimkan kueri yang dienkripsi.

# Eksekusi Permintaan HTTP:

# Setelah pembuatan permintaan HTTP dengan kueri yang sesuai, permintaan tersebut dikirim menggunakan metode makeHttpRequest.
# Hasil respons dari Bing diterima dan diuraikan untuk mendapatkan judul, URL, dan deskripsi dari setiap hasil pencarian.
# Jika hasil ditemukan, informasi situs ditampilkan dan URL ditambahkan ke cakupan Burp jika belum ada.

# Penanganan Galat:

# Program dilengkapi dengan penanganan galat sederhana yang mencetak pesan jika tidak ada hasil dari pencarian Bing.
# Alur program secara keseluruhan adalah menerima input dari pengguna dalam bentuk lalu lintas HTTP yang ditangkap, mengekstrak host atau IP dari input tersebut, melakukan pencarian Bing berdasarkan host atau IP tersebut, dan menampilkan hasilnya kepada pengguna.

# ======================================================================================================================================================================================================================================================================================== # 
    
# # Fungsi:
# Program ini berfungsi sebagai ekstensi untuk platform Burp Suite yang memungkinkan pengguna untuk melakukan pencarian informasi menggunakan layanan Bing terhadap host atau IP yang terdapat dalam lalu lintas HTTP yang ditangkap oleh Burp Suite. Dengan menggunakan program ini, pengguna dapat dengan mudah mengumpulkan informasi tambahan tentang host atau IP tertentu yang terlibat dalam lalu lintas HTTP.

# Manfaat:
# Analisis Keamanan: Memungkinkan analis keamanan untuk mendapatkan wawasan tambahan tentang host atau IP yang terlibat dalam lalu lintas HTTP. Ini dapat membantu dalam mendeteksi potensi kerentanan atau ancaman keamanan.

#Pencarian Informasi: Memudahkan pengguna untuk melakukan pencarian informasi tambahan tentang host atau IP tertentu tanpa meninggalkan lingkungan Burp Suite.

# Pengayaan Informasi: Memperkaya informasi yang terkandung dalam lalu lintas HTTP dengan informasi tambahan seperti judul halaman web, URL, dan deskripsi yang diperoleh dari hasil pencarian Bing.

# Cara Penggunaan:
    
# Instalasi Ekstensi: Ekstensi ini dapat diinstal di Burp Suite dengan menambahkannya melalui menu "Extender" -> "Extensions". Setelah diinstal, item menu "Send to Bing" akan muncul dalam menu konteks.

# Pemilihan Data: Pengguna harus memilih data lalu lintas HTTP yang ingin dicari informasinya. Hal ini dapat dilakukan dengan memilih data tersebut dalam panel "Proxy" atau "History" di Burp Suite.

# Eksekusi Pencarian: Setelah memilih data, pengguna dapat memilih item menu "Send to Bing" dari menu konteks. Ini akan memicu eksekusi pencarian menggunakan layanan Bing terhadap host atau IP yang terkandung dalam data yang dipilih.

# Pemrosesan Hasil: Setelah eksekusi pencarian selesai, hasilnya akan ditampilkan dalam konsol Burp Suite. Informasi seperti judul halaman web, URL, dan deskripsi akan ditampilkan untuk setiap hasil pencarian.

# Pengembangan:
# Pengoptimalan Kueri: Pengembang dapat memperluas fungsionalitas program dengan menambahkan opsi untuk mengoptimalkan kueri yang dikirim ke layanan Bing. Misalnya, penggunaan filter tambahan untuk mempersempit hasil pencarian.

# Pengayaan Informasi: Program ini saat ini hanya menampilkan informasi dasar seperti judul, URL, dan deskripsi. Pengembang dapat mempertimbangkan untuk memperkaya informasi yang ditampilkan dengan menambahkan elemen-elemen tambahan seperti informasi tentang domain, lokasi geografis, dan sebagainya.

# Peningkatan Antarmuka Pengguna: Pengembang dapat meningkatkan antarmuka pengguna program ini dengan menambahkan fitur-fitur seperti dialog untuk mengatur preferensi, pemilihan opsi pencarian, dan lain-lain.

# Pengelolaan Galat: Program saat ini memiliki penanganan galat yang sederhana. Pengembang dapat memperbaiki atau meningkatkan penanganan galat untuk membuat program lebih tangguh dan dapat diandalkan.

# Dengan pengembangan lebih lanjut, program ini dapat menjadi alat yang lebih kuat dan berguna bagi para analis keamanan dalam pekerjaan mereka.

# ====================================================================================================================================================================================================================================================================================================================== # 
    
# 






