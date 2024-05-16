import cv2
from kamene.all import *

pictures_directory = "pic_carver/pictures"
faces_directory = "pic_carver/faces"
pcap_file = "bhp.pcap"


def face_detect(path, file_name):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4,
                                     cv2.CASCADE_SCALE_IMAGE, (20, 20)
                                     )
    if len(rects) == 0:
        return False
    rects[:, 2:] += rects[:, :2]

    # highlight the faces in the image
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite("%s/%s-%s" % (faces_directory, pcap_file, file_name), img)
    return True


def get_http_headers(http_payload):
    try:
        # split the headers off if it is HTTP traffic
        headers_raw = http_payload[:http_payload.index("\r\n\r\n") + 2]
        # break out the headers
        headers = dict(
            re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers_raw))
    except:
        return None
    if "Content-Type" not in headers:
        return None
    return headers


def extract_image(headers, http_payload):
    image = None
    image_type = None

    try:
        if "image" in headers['Content-Type']:
            # grab the image type and image body
            image_type = headers['Content-Type'].split("/")[1]
            image = http_payload[http_payload.index("\r\n\r\n") + 4:]
            # if we detect compression decompress the image
            try:
                if "Content-Encoding" in list(headers.keys()):
                    if headers['Content-Encoding'] == "gzip":
                        image = zlib.decompress(image, 16 + zlib.MAX_WBITS)
                    elif headers['Content-Encoding'] == "deflate":
                        image = zlib.decompress(image)
            except:
                pass
    except:
        return None, None
    return image, image_type


def http_assembler(pcap_fl):
    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_fl)
    sessions = a.sessions()

    for session in sessions:
        http_payload = ""
        for packet in sessions[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    # reassemble the stream into a single buffer
                    http_payload += str(packet[TCP].payload)
            except:
                pass
        headers = get_http_headers(http_payload)

        if headers is None:
            continue

        image, image_type = extract_image(headers, http_payload)

        if image is not None and image_type is not None:
            # store the image
            file_name = "%s-pic_carver_%d.%s" % (
                pcap_fl, carved_images, image_type)
            fd = open("%s/%s" % (pictures_directory, file_name), "wb")
            fd.write(image)
            fd.close()
            carved_images += 1
            # now attempt face detection
            try:
                result = face_detect("%s/%s" % (pictures_directory, file_name),
                                     file_name)
                if result is True:
                    faces_detected += 1
            except:
                pass
    return carved_images, faces_detected


carved_img, faces_dtct = http_assembler(pcap_file)

print("Extracted: %d images" % carved_images)
print("Detected: %d faces" % faces_detected)


# ========================================================================================== # 

# Program ini merupakan skrip Python yang bertujuan untuk melakukan analisis terhadap data jaringan dalam sebuah file pcap. Pada dasarnya, program ini melakukan proses ekstraksi terhadap gambar yang dikirimkan melalui protokol HTTP dalam file pcap, kemudian mencoba mendeteksi wajah dalam gambar-gambar tersebut.

# Berikut adalah alur programnya:

# Import Library: Program mengimpor modul cv2 (OpenCV) untuk pemrosesan gambar dan modul kamene untuk manipulasi paket jaringan.

# Inisialisasi Variabel: Variabel pictures_directory, faces_directory, dan pcap_file diinisialisasi untuk menentukan direktori penyimpanan gambar, direktori penyimpanan wajah, dan file pcap yang akan dianalisis.

# face_detect Function: Fungsi ini digunakan untuk mendeteksi wajah dalam suatu gambar. Pertama, gambar dibaca menggunakan OpenCV. Kemudian, dilakukan deteksi wajah menggunakan classifier Haar Cascade. Jika wajah terdeteksi, gambar akan disimpan dengan kotak pembatas pada wajah. Fungsi ini mengembalikan True jika wajah terdeteksi, dan False jika tidak.

# get_http_headers Function: Fungsi ini mengembalikan header HTTP dari payload yang diberikan. Header dipisahkan dari payload HTTP menggunakan \r\n\r\n, lalu dipecah menjadi dictionary. Jika header tidak ada atau tidak lengkap, fungsi mengembalikan None.

# extract_image Function: Fungsi ini bertujuan untuk mengekstrak gambar dari payload HTTP. Jika payload mengandung gambar (berdasarkan header Content-Type), maka fungsi ini akan mengembalikan tipe gambar dan isi gambar tersebut.

# http_assembler Function: Fungsi ini melakukan perakitan ulang paket HTTP dari file pcap yang diberikan. Setiap paket HTTP digabungkan menjadi satu payload. Kemudian, fungsi get_http_headers dipanggil untuk mendapatkan header HTTP. Jika header ditemukan, fungsi extract_image dipanggil untuk mengekstrak gambar dari payload. Gambar yang berhasil diekstrak akan disimpan dalam direktori yang ditentukan, dan jika ada wajah yang terdeteksi dalam gambar tersebut, gambar juga akan disimpan dalam direktori wajah. Fungsi ini mengembalikan jumlah gambar yang diekstrak dan jumlah wajah yang terdeteksi.

# Eksekusi: Fungsi http_assembler dipanggil dengan argumen file pcap yang ditentukan sebelumnya. Hasil ekstraksi dan deteksi wajah kemudian dicetak.

# Ada beberapa potensi perbaikan dalam kode, misalnya, variabel carved_images dan faces_detected seharusnya digunakan untuk mencetak hasil, bukan carved_img dan faces_dtct, karena variabel tersebut tidak didefinisikan sebelumnya.

# ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================== # 

# Fungsi face_detect:
# Manfaat:

# Fungsi ini digunakan untuk mendeteksi wajah dalam sebuah gambar.
# Berguna dalam proses analisis gambar untuk pengenalan objek atau identifikasi orang.

# Cara Penggunaan:

# Memanggil fungsi face_detect dengan menyediakan path ke gambar yang akan dianalisis.
# Fungsi akan mengembalikan True jika wajah terdeteksi dalam gambar, dan False jika tidak.

# Pengembangan:

# Meningkatkan akurasi deteksi wajah dengan menggunakan classifier yang lebih canggih atau dilatih lebih baik.
# Menambah fitur untuk mendeteksi atribut wajah lainnya seperti mata, hidung, atau mulut.
# Integrasi dengan sistem pengenalan wajah untuk mengidentifikasi individu dalam gambar.

# Fungsi get_http_headers:

# Manfaat:

# Fungsi ini digunakan untuk mendapatkan header HTTP dari sebuah payload.
# Berguna dalam analisis trafik jaringan untuk memahami jenis konten yang dikirimkan.

# Cara Penggunaan:

# Memanggil fungsi get_http_headers dengan menyediakan payload HTTP.
# Fungsi akan mengembalikan dictionary yang berisi header HTTP.

# Pengembangan:

# Penanganan yang lebih baik terhadap kasus-kasus yang tidak terduga dalam pembacaan header HTTP.
# Penambahan fitur untuk memperoleh lebih banyak informasi dari header HTTP yang ditemukan.
# Integrasi dengan sistem analisis trafik jaringan yang lebih besar.
# Fungsi extract_image:

# Manfaat:

# Fungsi ini digunakan untuk mengekstrak gambar dari sebuah payload HTTP.
# Berguna dalam proses analisis konten jaringan untuk menemukan dan menyimpan gambar yang dikirimkan.

# Cara Penggunaan:

# Memanggil fungsi extract_image dengan menyediakan header HTTP dan payload HTTP.
# Fungsi akan mengembalikan gambar yang diekstrak beserta tipe gambar tersebut.

# Pengembangan:

# Penanganan yang lebih baik terhadap jenis kompresi gambar yang berbeda.
# Penambahan dukungan untuk ekstraksi konten multimedia lainnya seperti video atau audio.
# Integrasi dengan sistem penyimpanan atau analisis konten jaringan yang lebih luas.

# Fungsi http_assembler:

# Manfaat:

# Fungsi ini digunakan untuk merakit ulang paket-paket HTTP dari sebuah file pcap.
# Berguna dalam proses analisis trafik jaringan untuk memahami komunikasi yang terjadi.

# Cara Penggunaan:

# Memanggil fungsi http_assembler dengan menyediakan file pcap yang akan dianalisis.
# Fungsi akan mengembalikan jumlah gambar yang berhasil diekstrak dan jumlah wajah yang terdeteksi dalam gambar tersebut.

# Pengembangan:

# Peningkatan efisiensi dalam merakit ulang paket-paket HTTP, terutama untuk file pcap yang sangat besar.
# Penambahan fitur untuk analisis konten lainnya selain gambar.
# Integrasi dengan sistem visualisasi atau pemrosesan data yang lebih canggih.



