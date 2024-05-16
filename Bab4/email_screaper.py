from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
# Program ini adalah crawler web sederhana yang menggunakan BeautifulSoup dan requests untuk mengekstrak email dari halaman web yang ditentukan oleh pengguna. 
user_url = str(input('[+] Masukan URL Target Untuk Memindai: '))
urls = deque([user_url])
# 1. **Input**: Pengguna diminta untuk memasukkan URL target yang akan dipindai.
scraped_urls = set()
emails = set()
# 2. **Inisialisasi Variabel**: Program menginisialisasi deque `urls` yang berisi URL target untuk dipindai, serta set `scraped_urls` dan `emails` untuk menyimpan URL yang telah dipindai dan email yang ditemukan.
count = 0
try:
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print('[%d] Memproses! %s' % (count, url))
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")
        # 3. **Loop Melalui Setiap URL**:
        #      - Program memulai loop while untuk memproses setiap URL dalam deque `urls`.
        #        Selama proses, program mengekstrak email dari halaman web menggunakan ekspresi reguler dan menambahkannya ke dalam set `emails`.
        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)
                # 4. **Memindai Tautan**: Program menggunakan BeautifulSoup untuk menemukan semua tautan (`<a>` tags) dalam halaman web. Kemudian, untuk setiap tautan, program memeriksa apakah tautan itu adalah tautan internal (dimulai dengan `/`) atau tautan eksternal. Jika tautan tersebut belum dipindai atau sudah terpindai, program menambahkannya ke dalam deque `urls` untuk diproses nanti.
except KeyboardInterrupt:
    print('[-] Penutupan!')
# 5. **Exception Handling**: Program menangani pengecualian seperti `KeyboardInterrupt` dan kesalahan koneksi saat melakukan permintaan HTTP.
for mail in emails:
    print(mail)
# 6. **Output**: Setelah selesai memindai, program mencetak semua email yang ditemukan.

# Dengan cara ini, program membantu pengguna dalam menemukan email yang terkandung dalam halaman web yang ditentukan, serta tautan yang ada di halaman web tersebut.
# ================================================================================================================================================================================= 