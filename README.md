<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h2>Python 3 Hacking</h2>

<p>Python3-hacking yang sudah sepenuhnya dikonversi ke Python 3, diformat ulang untuk mematuhi standar PEP8 dan difaktorkan ulang untuk menghilangkan masalah ketergantungan yang melibatkan penerapan perpustakaan yang tidak digunakan lagi.</p>

<h2>Penggunaan</h2>

<p>Cukup pilih direktori (DIR) untuk mengkloning proyek yang digunakan <code>git clone</code>, buat lingkungan virtual baru atau <code>venv</code> untuknya (disarankan) dan instal persyaratan menggunakan <code>pip install</code>.</p>

<pre>
<code>pengguna@host:~/DIR$ git clone https://github.com/Yoga913/Python3-Hacking
pengguna@host:~/DIR$ python3 -m venv venv
pengguna@host:~/DIR$ source venv/bin/activate
(venv) pengguna@host:~/DIR$ pip install -r requirements.txt
</code>
</pre>

<h2>Pemfaktoran ulang</h2>

<p>Perbaikan bug penting yang harus dilakukan agar dapat mengimplementasikan dengan benar kode sumber dan menghindari kesalahan fatal:</p>

<ul>
    <li><code>chapter02/bh_sshserver.py</code> memerlukan kunci RSA yang terdapat dalam file <code>test_rsa.key</code>, sekarang disertakan dalam direktori terkait.</li>
    <li><code>chapter03/sniffer_ip_header_decode.py</code> & <code>sniffer_with_icmp.py</code> & <code>scanner.py</code> semuanya serius masalah dalam definisi ukuran paket IP dan portabilitas antara 32/64-bit arsitektur karena masalah dalam implementasi <code>struct</code>. Lebih lanjut tentang ini masalah di <a href="https://stackoverflow.com/questions/29306747/python-sniffing-from-black-hat-python-book#29307402">utas ini di Stack Overflow.</a></li>
    <li><code>chapter03/scanner.py</code> menggunakan perpustakaan <code>netaddr</code>, padahal bukan dipertahankan lagi dan menghadirkan banyak ketidakcocokan dengan Python 3. Oleh karena itu kode tersebut telah difaktorkan ulang dan sekarang menggunakan <code>ipaddress</code> modul dari <code>stdlib</code> Python.</li>
    <li><code>chapter04/arper.py</code> & <code>mail_sniffer.py</code> menggunakan perpustakaan <code>scapy</code>, yaitu tidak kompatibel dengan Python 3. Oleh karena itu, kode tersebut telah difaktorkan ulang dan sekarang menggunakan perpustakaan <code>kamene</code>.</li>
    <li><code>chapter04/pic_carver.py</code> sekarang menggunakan perpustakaan <code>opencv-python</code> sebagai ganti <code>cv2</code>. Modul "cv2.cv" tidak digunakan lagi dan telah diganti. Parameternya "cv2.cv.CV_HAAR_SCALE_IMAGE" dari kode asli digantikan oleh "cv2.CASCADE_SCALE_IMAGE" karena <a href="https://github.com/ragulin/face-recognition-server/commit/7b9773be352cbcd8a3aff50c7371f8aaf737bc5c">komit ini</a>.</li>
    <li><code>chapter05/content_bruter.py</code> memerlukan daftar kata agar dapat berfungsi. Itu telah ditambahkan ke bab di bawah <code>all.txt</code></li>
    <li><code>chapter05/joomla_killer.py</code> memerlukan daftar kata agar dapat berfungsi. Itu telah ditambahkan ke bab di bawah <code>cain.txt</code></li>
    <li><code>chapter06/bhp_bing.py</code> & <code>bhp_fuzzer.py</code> & <code>bhp_wordlist.py</code> telah diformat ulang untuk mematuhi PEP8, meskipun beberapa peringatan akan tetap ada dipicu karena kebutuhan untuk menyesuaikan nama kelas dengan casing unta aplikasi khusus ini di Burp Suite.</li>
    <li><code>chapter06/jython-standalone-2.7.2.jar</code> tersedia sebagai yang lebih diperbarui versi file relatif terhadap yang disajikan dalam buku.</li>
    <li><code>chapter07/git_trojan.py</code> telah difaktorkan ulang untuk menggantikan pustaka <code>imp</code> (sekarang tidak digunakan lagi) untuk <code>types</code>. Struktur subdirektori dengan yang diperlukan file konfigurasi telah diterapkan seperti yang diinstruksikan dalam buku. Itu Variabel "trojan_config" tidak memiliki jalur relatif ke subdirektori <code>config</code>. Panggilan ke metode "to_tree" ditambahkan ke baris 60 untuk hindari pengecualian AttributeError yang dihasilkan oleh kode asli. Petunjuk tentang cara membuat token akses alih-alih menggunakan kata sandi seseorang jika 2FA digunakan, kami disertakan sebagai komentar.</li>
    <li><code>chapter08/keylogger.py</code> memerlukan perpustakaan <code>PyHook</code> agar berfungsi. File roda telah disertakan dengan versi 1.6.2. Jika perlu, versi lain bisa dapat diunduh dari <a href="https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook">di sini</a>.</li>
    <li><code>chapter09/ie_exfil.py</code> menimbulkan kesalahan karena penanganan teks biasa variabel (yang dapat muncul sebagai string atau string biner) saat diserahkan ke fungsi "encrypt_string". Selain itu, penggunaan perpustakaan <code>base64</code> adalah dikoreksi. <em>Kontribusi dari <a href="https://github.com/Enraged">Enraged</a> di <a href="https://github.com/EONRaider/blackhat-python3/pull/2/commits/fcab6afc19fc4ea01b8c5c475e7b8c5e4b158df6">komit ini</a>.</em></li>
</ul>

</body>
</html>
