# Program ini adalah sebuah script untuk melakukan serangan brute force terhadap nilai hash yang diberikan.
import hashlib

type_of_hash = str(input('Jenis hash mana yang ingin Anda bruteforce ?'))
file_path = str(input('Masukkan path ke file untuk bruteforce dengan: '))
hash_to_decrypt = str(input('Masukkan Nilai Hash Ke Bruteforce: '))
# 1. **Input**:
# - Pengguna diminta untuk memasukkan jenis hash yang akan diserang (MD5 atau SHA1), 
#   path ke file yang berisi daftar kata-kata untuk dilakukan brute force, dan nilai hash yang akan diserang.
with open(file_path, 'r') as file:
    # 2. **Buka File**: Program membuka file yang diberikan oleh pengguna dalam mode baca (`'r'`).
    for line in file.readlines(): # 3. **Loop Melalui Setiap Baris**: Program membaca setiap baris dalam file yang dibuka.
        if type_of_hash == 'md5':
            hash_object = hashlib.md5(line.strip().encode())
            hashed_word = hash_object.hexdigest()
            if hashed_word == hash_to_decrypt:
                print('Ditemukan MD5 Password: ' + line.strip())
                exit(0)

        if type_of_hash == 'sha1':
            hash_object = hashlib.sha1(line.strip().encode())
            hashed_word = hash_object.hexdigest()
            if hashed_word == hash_to_decrypt:
                print('Ditemukan SHA1 Pasword: ' + line.strip())
                exit(0)
                # 4. **Brute Force**: Untuk setiap kata dalam file, program melakukan hashing menggunakan algoritma yang sesuai dengan jenis hash yang dipilih oleh pengguna (MD5 atau SHA1). Hasil hashing dibandingkan dengan nilai hash yang diberikan. Jika ada kecocokan, program mencetak kata yang sesuai dan keluar dari program.

    print('KAta sandi tida dalam file.')

# 5. **Output**: Jika tidak ada kecocokan ditemukan setelah loop selesai, program mencetak pesan bahwa password tidak ada dalam file.

# Dengan cara ini, program memungkinkan pengguna untuk mencoba memecahkan nilai hash dengan menggunakan daftar kata-kata yang disediakan dalam file. Ini adalah pendekatan umum yang digunakan dalam serangan brute force untuk mencoba berbagai kemungkinan nilai sampai nilai yang cocok ditemukan.
# =====================================================================
