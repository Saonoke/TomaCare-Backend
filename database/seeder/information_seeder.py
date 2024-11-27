from certifi import contents

from model import Images, Information
from sqlmodel import Session, select


class InformationSeeder:

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def create_information():
        informations = [
            Information(
                id=1,
                title='Tomato Bacterial Spot',
                content='''
Deskripsi:
Penyakit ini disebabkan oleh bakteri Xanthomonas campestris pv. vesicatoria yang menyerang daun, batang, dan buah tomat. Penyakit ini sering terjadi dalam kondisi hangat dan lembap. Infeksi awal sering sulit dideteksi, namun cepat menyebar melalui air (percikan hujan atau penyiraman) atau peralatan yang terkontaminasi.

Detail Gejala:
- Bercak kecil berwarna cokelat gelap atau hitam dengan tepi berair pada daun.
- Bercak pada buah biasanya dangkal dan melingkar, dengan tekstur kasar.
- Pada infeksi berat, daun bisa gugur, meningkatkan risiko sunburn pada buah.

Penyebab:
- Penyebaran bakteri melalui biji terinfeksi, sisa tanaman, atau air.
                ''',
                medicine='Fungisida berbasis tembaga, seperti Copper Hydroxide atau Copper Oxychloride. Contoh produk: Nordox 75 WG, Kocide 3000.'
            ), Information(
                id=2,
                title='Tomato Early Blight',
                content='''
Deskripsi:
Penyakit ini disebabkan oleh jamur Alternaria solani, yang menyerang daun tua terlebih dahulu sebelum menyebar ke bagian tanaman lainnya. Penyakit ini umum di daerah dengan perubahan suhu yang drastis.

Detail Gejala:
- Bercak cokelat tua berbentuk bulat dengan pola lingkaran konsentris (seperti "mata banteng").
- Daun menguning di sekitar bercak, akhirnya rontok.
- Batang dan buah menunjukkan lesi hitam melingkar, terutama di dekat pangkal tangkai buah.

Penyebab:
- Penyebaran melalui spora yang terbawa angin, air, atau peralatan.
                ''',
                medicine='Fungisida berbasis Chlorothalonil (contoh: Daconil) atau Mancozeb. Produk sistemik seperti Azoxystrobin (contoh: Amistar Top) juga efektif.'
            ), Information(
                id=3,
                title='Tomato Late Blight',
                content='''
Deskripsi:
Late Blight adalah penyakit destruktif yang disebabkan oleh Phytophthora infestans. Penyakit ini sering menyebabkan kerusakan total jika tidak segera diatasi.

Detail Gejala:
- Daun menunjukkan bercak basah berwarna cokelat atau abu-abu dengan tepi hijau kekuningan.
- Bagian bawah daun sering ditutupi jamur putih, terutama di pagi hari.
- Buah menunjukkan bercak cokelat gelap, tekstur basah, dan akhirnya membusuk.

Penyebab:
- Penyebaran melalui spora yang terbawa angin dan air, terutama saat kelembapan tinggi.
                ''',
                medicine='Fungisida sistemik seperti Metalaxyl-M (contoh: Ridomil Gold) atau Dimethomorph (contoh: Acrobat). Kombinasikan dengan Copper Hydroxide untuk pencegahan.'
            ), Information(
                id=4,
                title='Tomato Leaf Mold',
                content='''
Deskripsi:
Penyakit ini sering menyerang tomat di rumah kaca atau daerah dengan ventilasi buruk. Disebabkan oleh jamur Cladosporium fulvum, penyakit ini lebih umum pada daun, tetapi bisa menyebar ke buah.

Detail Gejala:
- Bercak kuning pucat di bagian atas daun yang berubah menjadi cokelat.
- Bagian bawah daun menunjukkan lapisan beludru hijau zaitun atau cokelat.
- Dalam kasus berat, daun mengering, layu, dan rontok.

Penyebab:
- Penyebaran melalui spora udara, terutama dalam kelembapan tinggi.
                ''',
                medicine='Fungisida berbasis Sulfur (contoh: Thiovit Jet) atau produk seperti Tebuconazole untuk infeksi berat.'
            ), Information(
                id=5,
                title='Tomato Septoria Leaf Spot',
                content='''
Deskripsi:
Septoria Leaf Spot adalah penyakit jamur yang menyerang daun bagian bawah tanaman terlebih dahulu, mengurangi kemampuan fotosintesis dan memperlemah tanaman.

Detail Gejala:
- Bercak kecil bulat dengan pusat putih atau abu-abu dan tepi hitam pada daun.
- Infeksi berat menyebabkan daun menguning, mengering, dan akhirnya rontok.
- Tidak secara langsung memengaruhi buah, tetapi melemahkan tanaman secara keseluruhan.

Penyebab:
- Jamur menyebar melalui percikan air atau sisa tanaman yang terinfeksi.
                ''',
                medicine='Fungisida berbasis tembaga (seperti Nordox) atau Chlorothalonil (contoh: Bravo Weather Stik). Difenoconazole juga efektif.'
            ), Information(
                id=6,
                title='Tomato Spider Mites',
                content='''
Deskripsi:
Tungau laba-laba ini sangat kecil dan sering tak terlihat dengan mata telanjang. Serangga ini menyerang bagian bawah daun, menyedot cairan tanaman.

Detail Gejala:
- Daun menunjukkan bercak putih kecil (gigitan tungau) yang akhirnya menguning.
- Kehadiran jaring laba-laba halus di bagian bawah daun.
- Daun layu dan gugur pada serangan berat.

Penyebab:
- Penyebaran dipicu oleh cuaca kering dan panas.
                ''',
                medicine='Minyak neem (contoh: Neemix) atau insektisida berbasis Abamectin (contoh: Agrimek). Alternatif alami melibatkan pelepasan predator seperti Phytoseiulus persimilis.'
            ), Information(
                id=7,
                title='Tomato Target Spot',
                content='''
Deskripsi:
Target Spot disebabkan oleh jamur Corynespora cassiicola yang menyerang daun, batang, dan buah. Penyakit ini dapat menurunkan hasil panen secara signifikan.

Detail Gejala:
- Bercak melingkar berwarna cokelat gelap dengan lingkaran konsentris pada daun.
- Buah menunjukkan lesi kecil yang meluas, menyebabkan kerusakan permanen.
- Pada serangan berat, daun rontok, dan batang menunjukkan lesi panjang.

Penyebab:
- Penyebaran melalui sisa tanaman atau spora yang terbawa angin.
                ''',
                medicine='Fungisida berbasis Mancozeb (contoh: Dithane M-45) atau Chlorothalonil (contoh: Bravo Weather Stik). Untuk infeksi berat, gunakan Fluopyram (contoh: Luna Tranquility).'
            ), Information(
                id=8,
                title='Tomato Tomato Yellow Leaf Curl Virus (TYLCV)',
                content='''
Deskripsi:
Penyakit ini merupakan infeksi virus yang ditularkan oleh kutu kebul (Bemisia tabaci). TYLCV sangat merusak, terutama di wilayah tropis dan subtropis.

Detail Gejala:
- Daun muda menggulung ke atas, berubah warna kuning terang.
- Tanaman kerdil dan pertumbuhan terhambat.
- Produksi buah berkurang atau tidak ada sama sekali.

Penyebab:
- Penyebaran melalui kutu kebul atau biji yang terinfeksi.
                ''',
                medicine='Tidak ada obat langsung untuk virus, tetapi kutu putih (vektor virus) dapat dikendalikan menggunakan insektisida berbasis Imidacloprid atau Pyriproxyfen. Contoh produk: Confidor, Admiral.'
            ), Information(
                id=9,
                title='Tomato Tomato Mosaic Virus (ToMV)',
                content='''
Deskripsi:
Penyakit virus ini menyerang daun dan buah, menghambat pertumbuhan tanaman secara signifikan. Virus ini mudah menyebar melalui kontak langsung.

Detail Gejala:
- Daun menunjukkan pola belang hijau muda dan tua.
- Pertumbuhan tanaman terhambat, dengan daun yang melengkung.
- Buah sering memiliki bercak tidak merata dan kualitasnya menurun.

Penyebab:
- Penyebaran melalui alat yang terkontaminasi, biji, atau tangan manusia.
                ''',
                medicine='Tidak ada fungisida spesifik, tetapi aplikasi produk berbasis deterjen atau desinfektan (contoh: Virkon S) pada alat dan permukaan dapat membantu mencegah penyebaran.'
            )
        ]

        return informations

    def clear(self):
        informations = self.session.exec(select(Information)).all()

        for information in informations:
            self.session.delete(information)
        self.session.commit()

    def execute(self):
        informations = self.create_information()
        for information in informations:
            self.session.add(information)
        self.session.commit()
