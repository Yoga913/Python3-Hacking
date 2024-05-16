from Crypto.PublicKey import RSA


new_key = RSA.generate(2048)

public_key = new_key.publickey().exportKey("PEM")
private_key = new_key.exportKey("PEM") 

print(public_key)
print(private_key)

# ============================================================ # 
# Kode yang Anda berikan menggunakan pustaka kriptografi Crypto untuk menghasilkan pasangan kunci RSA, yaitu kunci publik dan kunci privat. Berikut penjelasan singkatnya:

# 1. from Crypto.PublicKey import RSA
# Ini adalah pernyataan impor yang mengimpor kelas RSA dari modul Crypto.PublicKey, yang merupakan bagian dari pustaka kriptografi Crypto.

# 2. new_key = RSA.generate(2048)
# Baris ini menghasilkan pasangan kunci RSA baru dengan panjang kunci 2048 bit. Fungsi generate() digunakan untuk membuat kunci baru dengan panjang tertentu.

# 3. public_key = new_key.publickey().exportKey("PEM")
# Di sini, publickey() digunakan untuk mendapatkan kunci publik dari new_key. Kemudian, metode exportKey() digunakan untuk mengekspor kunci publik dalam format PEM (Privacy Enhanced Mail), yang merupakan format umum untuk menyimpan kunci publik.

# 4. private_key = new_key.exportKey("PEM")
# Ini mirip dengan baris sebelumnya, kecuali bahwa ini mengekspor kunci privat, bukan kunci publik.

# 5. print(public_key)
# Ini mencetak kunci publik yang baru dihasilkan ke konsol.

# 6. print(private_key)
# Ini mencetak kunci privat yang baru dihasilkan ke konsol.

# Jadi, secara keseluruhan, kode tersebut menghasilkan pasangan kunci RSA baru, mengekspor kunci publik dan kunci privat dalam format PEM, dan mencetak keduanya ke konsol. Kunci-kunci ini dapat digunakan untuk enkripsi, dekripsi, dan tanda tangan digital dalam aplikasi kriptografi.




