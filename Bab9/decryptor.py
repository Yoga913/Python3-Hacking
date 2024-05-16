import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

encrypted = """XxfaX7nfQ48K+l0rXM3tQf3ShFcytAQ4sLe6vn8bWdreho4riaJ5Dy5PeijSKbsgWSMoeZLmihxb0YAFgCaIp11AUl4kmIiY+c+8LJonbTTembxv98GePM1SEme5/vMwGORJilw+rTdORSHzwbC56sw5NG8KosgLWwHEGEGbhii2qBkuyQrIc9ydoOKKCe0ofTRnaI2c/lb9Ot3vkEIgxCks94H6qVkAfhO34HS7nClUldn9UN040RYgtEqBgvAFzoEhDuRtfjJu1dzyzaFtRAVhcQ6HdgZMWRfpaxKQOmbhXwYyGRQfwNl/Rwgn1EJBFAhvIaEifHDlCw+hLViNYlae7IdfIb6hWtWPyFrkaNjmkbhhXclNgZe0+iPPDzsZbpHI1IckG0gVlTdlGKGz+nK5Cxyso41icC4gO7tmdXDGgF6bMt/GC1VjMVmL/rYsb8jzJblmuQBAeFNacyhjxrzIH5v60RQ1BxwfD+wLCKfyzn3vQucPak2cnwBs3yTIEShYj0ymP4idU/5Qt5qkqMDyvO4U8DmqB4KT58+o2B3c88+lUZjz7c9ygwKjp2hSNf+Dm9H3YJY2Pn6YlydyT1sYWCy06DZko7z3uae5GYGjez8hnCIFt+mpeLvEelSHeZfyV8wYyHg5Y9eA2NZNX6yNVD8IREhjXGWdbGTn41lVCqEiCetY9SKdWeL1Hp/vJN3SOo4qglbQF7P6oqqg0bofnAcphLVaHw/FOGWtW1CFEQUQdIg9bk+SJqM/s1ozJlisenrRzxv3L5LthEfLflCafK0u3n2gPa4F3ok4tx9i+r+MykRTw+OksMfVu71CAMuJdrFQLMSpyWkQ86Vc/QIXgdoCKkAYx5xr/U8gDXkZ4GvL9biEZv/fb5Wh7Br1Hu6idUgTYpEJVVnMuI13ePGeJLA54Il2S7aDyrgfhb61WQmoMRGvLP7uxCjgLwrxZNjAYJTmXszLvvgmI+lHe5o8rgQw6zSGpl9k27urV4bA0Zt+PsYiLNbEQqqxrJxKcbKqozl8XtfMXanct9pKu4vaq8fH/j9jvZ133UtcaR5iTQ0K7P4J5Qoaxz3uUhGrgplZ1jE9Nr0iyRj722dW82b4m1f/h80K7EuvwEeOfdYZl7iFL8yRi9dfopwATjKbKrWFroGCb/wvpc5ujpzDfwAeWsSU4Nve2qBDo5coVt1GI8rzHUh52TQ007JhcYABIxZGSFeeJ3bFgvqO2kUK/Pc36Au0VlNFds/j+fIuMlmFUuckBLCTpE2W9hYqmVOWBmyeZPJNzVI4gLexFbXbg8+0Eq6Pa4MxZsR3wypgC9LE/dvLbQ3oSn9x7nKMXpdq9r+xK1sjodpeYNz7t/5GpFu1teN0SFbmsoXjVEyOAn3L5Gd4Wxua7y9xOixc1H2/bbyNqJZAjEm34DDmNRTQtrqCwOEXwFGKgRGUzPYGC74wAPDDTaQEBv7Toc7rfkzgRX4ROW0SUaEPmi5tAlXe+CKVdJGtLKXUXYRHLMZ4jTzGsD89dmt2r2Fh6AUUN2e9jzzK2ULMnMhRUnDdcM74jbuDHGtXt56pFxFKJ21FQFS8JK0ZOqYa+0JjLuSzrLN9gSCu/JuTPC60LTxLsLcWZVR7cIHQE+sgDtt40/6O1YE7/8rs6qB9re28gDY1s9R5HFtjowO3ylRWqlaV9MC1OGzM4xHPxG2V+2zuq6ol8Cs="""

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAyXUTgFoL/2EPKoN31l5Tlak7VxhdusNCWQKDfcN5Jj45GQ1o
ZZjsECQ8jK5AaQuCWdmEQkgCEV23L2y71G+Th/zlVPjp0hgC6nOKOuwmlQ1jGvfV
vaNZ0YXrs+sX/wg5FT/bTS4yzXeW6920tdls2N7Pu5N1FLRW5PMhk6GW5rzVhwdD
vnfaUoSVj7oKaIMLbN/TENvnwhZZKlTZeK79ix4qXwYLe66CrgCHDf4oBJ/nO1oY
welxuIXVPhIZnVpkbz3IL6BfEZ3ZDKzGeRs6YLZuR2u5KUbr9uabEzgtrLyOeoK8
UscKmzOvtwxZDcgNijqMJKuqpNZczPHmf9cS1wIDAQABAoIBAAdOiMOKAI9lrNAk
7o7G4w81kSJqjtO8S0bBMZW5Jka90QJYmyW8MyuutMeBdnKY6URrAEILLJAGryM4
NWPSHC69fG/li02Ec26ffC8A67FSR/rtbEIxj4tq6Q6gg0FLwg5EP6b/+vW61a1+
YBSMa0c+ZZhvE7sJg3FQZDJflQKPXFHYxOlS42+UyUP8K07cFznsQCvia9mCHUG6
BDFbV/yjbMyYgKTCVmMeaCS2K0TlbcyGpF0Bz95mVpkrU6pHXY0UAJIv4dyguywe
dBZcJlruSRL0OJ+3Gb3CJS7YdsPW807LSyf8gcrHMpgV5z2CdGlaoaLBJyS/nDHi
n07PIbECgYEA4Rjlet1xL/Sr9HnHVUH0m1iST0SrLlQCzrMkiw4g5rCOCnhWPNQE
dpnRpgUWMhhyZj82SwigkdXC2GpvBP6GDg9pB3Njs8qkwEsGI8GFhUQfKf8Bnnd2
w3GUHiRoJpVxrrE3byh23pUiHBdbp7h2+EaOTrRsc2w3Q4NbNF+FOOkCgYEA5R1Z
KvuKn1Sq+0EWpb8fZB+PTwK60qObRENbLdnbmGrVwjNxiBWE4BausHMr0Bz/cQzk
tDyohkHx8clp6Qt+hRFd5CXXNidaelkCDLZ7dasddXm1bmIlTIHjWWSsUEsgUTh7
crjVvghU2Sqs/vCLJCW6WYGb9JD2BI5R9pOClb8CgYEAlsOtGBDvebY/4fwaxYDq
i43UWSFeIiaExtr30+c/pCOGz35wDEfZQXKfF7p6dk0nelJGVBVQLr1kxrzq5QZw
1UP/Dc18bvSASoc1codwnaTV1rQE6pWLRzZwhYvO8mDQBriNr3cDvutWMEh4zCpi
DMJ9GDwCE4DctuxpDvgXa9kCgYEAuxNjo30Qi1iO4+kZnOyZrR833MPV1/hO50Y4
RRAGBkX1lER9ByjK/k6HBPyFYcDLsntcou6EjFt8OnjDSc5g2DZ9+7QKLeWkMxJK
Yib+V+4Id8uRIThyTC4ifPN+33D4SllcMyhJHome/lOiPegbNMC5kCwMM33J455x
vmxjy/ECgYAOrFR7A9fP4QlPqFCQKDio/FhoQy5ERpl94lGozk4Ma+QDJiRUxA3N
GomBPAvYGntvGgPWrsEHrS01ZoOKGBfk5MgubSPFVI00BD6lccmff/0tOxYtb+Pp
vOGHt9D9yo3DOhyvJbedpi3u3g13G+FZFw6d1T8Jzm5eZUvG7WeUtg==
-----END RSA PRIVATE KEY-----"""

rsakey = RSA.importKey(private_key)
rsakey = PKCS1_OAEP.new(rsakey)

offset = 0
decrypted = ""
encrypted = base64.b64decode(encrypted)

while offset < len(encrypted):
    decrypted += rsakey.decrypt(encrypted[offset:offset + 256])
    offset += 256

# now we decompress to original
plaintext = zlib.decompress(decrypted)

print(plaintext)


# =========================================================================== 
# Program yang Anda berikan adalah skrip Python yang menggunakan beberapa modul kriptografi, yaitu zlib, base64, Crypto.PublicKey, dan Crypto.Cipher. Berikut adalah penjelasan alur program tersebut:

# Import modul yang diperlukan:

# import zlib
# import base64
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP
# Deklarasi variabel encrypted dan private_key. Variabel encrypted berisi data yang telah dienkripsi yang kemungkinan besar akan dienkripsi dengan kunci publik RSA, sedangkan private_key adalah kunci privat RSA yang akan digunakan untuk dekripsi data.

# encrypted = "__"  # Data yang telah dienkripsi (dalam bentuk string)
# private_key = "___"  # Kunci privat RSA
# Membuat objek RSA dari kunci privat yang diberikan:

# rsakey = RSA.importKey(private_key)
# Membuat objek PKCS1_OAEP yang akan digunakan untuk dekripsi:

# rsakey = PKCS1_OAEP.new(rsakey)
# Inisialisasi variabel offset dan decrypted untuk digunakan dalam proses loop dekripsi:


# offset = 0
# decrypted = ""
# Dekode data yang dienkripsi dari format base64:

# encrypted = base64.b64decode(encrypted)
# Looping melalui data yang dienkripsi dan mendekripsi setiap potongan menggunakan metode decrypt dari objek rsakey. Ukuran setiap potongan adalah 256 byte, sesuai dengan ukuran blok yang umum digunakan dalam enkripsi RSA:


# while offset < len(encrypted):
#     decrypted += rsakey.decrypt(encrypted[offset:offset + 256])
#     offset += 256

# Setelah data didekripsi, langkah selanjutnya adalah mendekompresi data menggunakan modul zlib:

# plaintext = zlib.decompress(decrypted)
# Cetak hasil dekompresi, yang merupakan teks asli yang telah dienkripsi dan kemudian didekompresi:


# print(plaintext)
# Dengan demikian, program ini mengambil data yang telah dienkripsi, mendekripsi menggunakan kunci privat RSA yang diberikan, dan kemudian mendekompresi hasil dekripsi untuk mengembalikan teks asli.

# =============================================================================================================================================================================================================================== # 
# Mari kita bahas tentang fungsi, manfaat, cara penggunaan, dan pengembangan dari setiap komponen utama dalam program yang Anda berikan:

# 1. zlib
# Fungsi: Modul zlib adalah modul bawaan Python yang menyediakan fungsionalitas untuk kompresi dan dekompresi data menggunakan algoritma kompresi DEFLATE.

# Manfaat:
# Mengurangi ukuran data untuk penyimpanan yang lebih efisien.
# Mengurangi waktu transfer data melalui jaringan dengan mengurangi jumlah byte yang harus ditransmisikan.
# Meningkatkan kinerja aplikasi yang memanipulasi data dalam jumlah besar.
# Cara Penggunaan: Menggunakan fungsi compress() untuk kompresi data dan decompress() untuk dekompresi data.
# Pengembangan: Mungkin untuk mengintegrasikan algoritma kompresi yang lebih efisien atau mengoptimalkan penggunaan zlib untuk skenario khusus.

# 2. base64
# Fungsi: Modul base64 digunakan untuk melakukan enkode dan dekode data ke dan dari format base64.

# Manfaat:
# Berguna untuk mengubah data biner menjadi format teks yang dapat ditransmisikan melalui protokol teks seperti email atau HTTP.
# Dapat digunakan untuk menyembunyikan atau mengubah data biner menjadi format yang lebih aman atau mudah diakses.
# Cara Penggunaan: Menggunakan fungsi b64encode() untuk enkode data dan b64decode() untuk dekode data.
# Pengembangan: Peningkatan efisiensi enkode/dekode data atau penggunaan alternatif untuk keamanan data.

# 3. Crypto.PublicKey RSA
# Fungsi: Modul Crypto.PublicKey dari pustaka pihak ketiga pycrypto menyediakan implementasi algoritma kunci publik, termasuk RSA.

# Manfaat:
# RSA adalah algoritma kriptografi kunci publik yang aman dan banyak digunakan untuk enkripsi dan dekripsi data serta untuk pembuatan dan verifikasi tanda tangan digital.
# Memungkinkan penggunaan kunci publik dan kunci privat untuk enkripsi dan dekripsi data.
# Cara Penggunaan: Membuat objek kunci RSA menggunakan importKey() dan melakukan operasi enkripsi/dekripsi dengan menggunakan objek tersebut.
# Pengembangan: Penambahan fitur keamanan tambahan, peningkatan kinerja, atau integrasi dengan implementasi kunci publik lainnya.

# 4. Crypto.Cipher PKCS1_OAEP
# Fungsi: Modul Crypto.Cipher dari pustaka pihak ketiga pycrypto menyediakan berbagai macam algoritma kriptografi untuk enkripsi dan dekripsi.

# Manfaat:
# Algoritma enkripsi PKCS1_OAEP adalah bagian dari standar PKCS #1 RSA dan menyediakan enkripsi yang aman dengan padding untuk melindungi terhadap serangan kriptografi yang berbasis padding.
# Berguna untuk enkripsi dan dekripsi data menggunakan kunci publik dan kunci privat RSA.
# Cara Penggunaan: Membuat objek enkripsi/dekripsi menggunakan PKCS1_OAEP.new() dan melakukan operasi enkripsi/dekripsi dengan menggunakan objek tersebut.
# Pengembangan: Peningkatan keamanan, peningkatan kinerja, atau integrasi dengan algoritma enkripsi lainnya.

# Dengan memahami fungsi, manfaat, cara penggunaan, dan potensi pengembangan dari setiap komponen ini, Anda dapat lebih baik memahami dan mengembangkan program kriptografi Anda. Selalu penting untuk mempertimbangkan keamanan dan kinerja saat mengembangkan atau menggunakan kriptografi dalam aplikasi Anda.






