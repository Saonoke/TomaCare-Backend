from fastapi import HTTPException
from sqlmodel import Session
from database.repository import TaskRepositoryMeta, TaskRepository
from database.schema import TaskBase, TaskCreate, TaskShow, TaskUpdate
from service import TaskServiceMeta
from enumeration import penyakitEnum
from datetime import date, timedelta
from model import Users, Plants

    



class TaskService(TaskServiceMeta):
    def __init__(self, user: Users, session:Session) :
        self.session = session
        self.user: Users = user
        self._task_repository : TaskRepositoryMeta = TaskRepository(self.session)

    def get_list(self,penyakit:penyakitEnum)-> list[TaskShow]:
         match penyakit:
                case penyakitEnum.bacterial_spot:
                   return [
                       [TaskShow(title='Buang daun yang memiliki bercak hitam kecil'),TaskShow(title='Bersihkan area di sekitar tanaman dari daun yang jatuh'),TaskShow(title='Semprotkan fungisida berbasis tembaga pada daun yang tersisa'),]
                       [
                    TaskShow(title='Hindari penyiraman dari atas, gunakan penyiraman langsung ke tanah'),
                    TaskShow(title='Pantau tanaman untuk bercak baru pada buah atau daun'),
                    TaskShow(title='Cek kondisi kelembapan tanah'),
                ],
                       [
                    TaskShow(title='Semprotkan insektisida alami untuk mengontrol serangga pembawa bakteri'),
                    TaskShow(title='Lakukan sanitasi alat berkebun sebelum digunakan'),
                    TaskShow(title='Periksa buah untuk bercak atau perubahan tekstur'),
                ],
                        [
                    TaskShow(title='Bersihkan gulma di sekitar tanaman'),
                    TaskShow(title='Lakukan inspeksi daun baru untuk mencegah penyebaran'),
                    TaskShow(title='Semprotkan ulang fungisida jika diperlukan'),
                ],
                       [
                    TaskShow(title='Pantau perubahan warna atau ukuran bercak pada daun yang tersisa'),
                    TaskShow(title='Semprotkan neem oil untuk mengontrol hama'),
                    TaskShow(title='Pastikan area sekitar tanaman tetap bersih dan bebas gulma'),
                ],
                       [
                    TaskShow(title='Periksa apakah daun yang dirawat menunjukkan tanda pemulihan'),
                    TaskShow(title='Cek tanaman lain di sekitar untuk mencegah penyebaran'),
                    TaskShow(title='Semprotkan ulang insektisida alami jika serangga masih ada'),
                ],
                       [
                    TaskShow(title='Dokumentasikan hasil pemantauan mingguan'),
                    TaskShow(title='Evaluasi keefektifan fungisida yang digunakan'),
                    TaskShow(title='Tentukan langkah perawatan selanjutnya sesuai gejala yang tersisa'),
                ],
                       ]
                case penyakitEnum.early_blight:
                  return [
                       [
                    TaskShow(title='Buang daun dengan lesi coklat berbentuk lingkaran konsentris'),
                    TaskShow(title='Semprotkan fungisida berbasis tembaga pada semua tanaman'),
                    TaskShow(title='Pastikan area sekitar tanaman bebas gulma'),
                ],
                       [
                    TaskShow(title='Periksa kelembapan tanah dan tambahkan air jika diperlukan'),
                    TaskShow(title='Pantau daun baru untuk mendeteksi gejala tambahan'),
                    TaskShow(title='Gunakan mulsa untuk menjaga kelembapan tanah'),
                ],
                      [
                    TaskShow(title='Semprotkan ulang fungisida pada daun yang terlihat terinfeksi'),
                    TaskShow(title='Lakukan sanitasi alat setelah digunakan'),
                    TaskShow(title='Periksa tanda-tanda kerusakan baru pada buah'),
                ],
                       [
                    TaskShow(title='Pantau lingkungan sekitar tanaman untuk mencegah penyebaran'),
                    TaskShow(title='Periksa kondisi drainase untuk memastikan air tidak menggenang'),
                    TaskShow(title='Lakukan penyiraman pagi hari untuk menjaga kelembapan optimal'),
                ],
                       [
                    TaskShow(title='Tambahkan pupuk organik untuk memperkuat daya tahan tanaman'),
                    TaskShow(title='Semprotkan neem oil untuk mencegah serangan hama'),
                    TaskShow(title='Pantau efektivitas fungisida yang digunakan'),
                ],
                      [
                    TaskShow(title='Buang daun yang menunjukkan gejala baru atau lebih parah'),
                    TaskShow(title='Semprotkan fungisida ulang jika infeksi meluas'),
                    TaskShow(title='Lakukan inspeksi ulang pada area sekitar tanaman'),
                ],
                       [
                    TaskShow(title='Dokumentasikan semua langkah yang telah dilakukan'),
                    TaskShow(title='Catat tanaman yang menunjukkan tanda pemulihan'),
                    TaskShow(title='Tentukan tindakan lanjutan untuk minggu berikutnya'),
                ],
                       ]
                case penyakitEnum.late_blight:
                  return [
                        [
                    TaskShow(title='Buang daun atau tanaman dengan lesi coklat kehijauan'),
                    TaskShow(title='Semprotkan fungisida sistemik pada semua tanaman'),
                    TaskShow(title='Lakukan sanitasi area sekitar tanaman'),
                ],
                [
                    TaskShow(title='Pantau daun baru untuk mendeteksi lesi tambahan'),
                    TaskShow(title='Periksa kelembapan tanah untuk memastikan drainase yang baik'),
                    TaskShow(title='Bersihkan gulma di sekitar tanaman'),
                ],
                [
                    TaskShow(title='Semprotkan ulang fungisida pada tanaman yang menunjukkan gejala'),
                    TaskShow(title='Periksa buah untuk tanda-tanda infeksi'),
                    TaskShow(title='Pastikan tidak ada genangan air di sekitar tanaman'),
                ],
                [
                    TaskShow(title='Pantau gejala tambahan pada daun yang sebelumnya sehat'),
                    TaskShow(title='Gunakan mulsa untuk mencegah penyebaran spora jamur'),
                    TaskShow(title='Lakukan sanitasi alat berkebun setelah digunakan'),
                ],
                [
                    TaskShow(title='Tambahkan pupuk organik untuk meningkatkan daya tahan tanaman'),
                    TaskShow(title='Semprotkan neem oil untuk mencegah serangan hama tambahan'),
                    TaskShow(title='Lakukan inspeksi ulang pada semua tanaman'),
                ],
                [
                    TaskShow(title='Semprotkan fungisida ulang jika gejala menyebar'),
                    TaskShow(title='Buang daun yang menunjukkan gejala baru'),
                    TaskShow(title='Periksa kondisi lingkungan di sekitar kebun'),
                ],
                [
                    TaskShow(title='Dokumentasikan hasil pemantauan mingguan'),
                    TaskShow(title='Catat tanaman yang menunjukkan tanda pemulihan'),
                    TaskShow(title='Rencanakan langkah perawatan untuk minggu berikutnya'),
                ],
                       ]
                case penyakitEnum.leaf_mold:
                  return [
                       [TaskShow(title='Potong daun yang memiliki bercak kuning atau jamur hijau'),
         TaskShow(title='Lakukan inspeksi menyeluruh pada tanaman')],
        [TaskShow(title='Semprotkan fungisida berbasis sulfur'),
         TaskShow(title='Pastikan area sekitar memiliki ventilasi yang baik')],
        [TaskShow(title='Pantau daun baru untuk gejala tambahan'),
         TaskShow(title='Lakukan sanitasi lingkungan tanaman')],
        [TaskShow(title='Gunakan air yang tidak terlalu dingin untuk penyiraman pagi hari'),
         TaskShow(title='Jaga kelembapan udara agar tidak terlalu tinggi')],
        [TaskShow(title='Semprotkan fungisida ulang jika jamur masih terlihat'),
         TaskShow(title='Bersihkan gulma dan sisa daun yang terinfeksi')],
        [TaskShow(title='Lakukan inspeksi tambahan di bagian bawah daun'),
         TaskShow(title='Evaluasi keberhasilan penanganan dan dokumentasikan')],
        [TaskShow(title='Diskusikan dengan ahli agronomi jika gejala tidak membaik'),
         TaskShow(title='Rencanakan langkah pengendalian lanjutan untuk minggu berikutnya')]
                       ]
                case penyakitEnum.septorial_leaf_spot:
                  return [
                       [TaskShow(title='Buang daun dengan bercak coklat kecil'),
         TaskShow(title='Lakukan inspeksi pada tanaman sekitarnya')],
        [TaskShow(title='Semprotkan fungisida berbasis tembaga'),
         TaskShow(title='Pastikan jarak antar tanaman cukup')],
        [TaskShow(title='Pantau perkembangan bercak baru di daun sehat'),
         TaskShow(title='Bersihkan sisa tanaman yang jatuh di tanah')],
        [TaskShow(title='Gunakan penyiraman langsung ke tanah untuk menghindari membasahi daun'),
         TaskShow(title='Sterilkan alat berkebun setelah digunakan')],
        [TaskShow(title='Semprotkan fungisida ulang jika diperlukan'),
         TaskShow(title='Lakukan pengamatan tambahan pada bagian bawah daun')],
        [TaskShow(title='Gunakan mulsa untuk mencegah percikan tanah ke daun'),
         TaskShow(title='Pantau kelembapan tanah agar tidak terlalu kering')],
        [TaskShow(title='Dokumentasikan hasil inspeksi mingguan'),
         TaskShow(title='Bersihkan area sekitar untuk mengurangi risiko infeksi ulang')]
                       ]
                case penyakitEnum.spidermites_two_spottedspider_mite:
                  return [
                       [TaskShow(title='Semprotkan air langsung ke tanaman untuk menghilangkan tungau'),
         TaskShow(title='Pantau tanaman untuk melihat jaring laba-laba halus')],
        [TaskShow(title='Semprotkan neem oil atau insektisida alami'),
         TaskShow(title='Pastikan area sekitar bersih dari debu atau kotoran')],
        [TaskShow(title='Lakukan inspeksi daun bagian bawah untuk mendeteksi tungau tambahan'),
         TaskShow(title='Semprotkan air ulang jika tungau masih terlihat')],
        [TaskShow(title='Tambahkan predator alami seperti kumbang ladybug jika memungkinkan'),
         TaskShow(title='Semprotkan neem oil ulang jika infestasi masih ada')],
        [TaskShow(title='Gunakan tisu basah untuk membersihkan daun yang terinfeksi parah'),
         TaskShow(title='Pantau tanaman sehat untuk mencegah penyebaran')],
        [TaskShow(title='Semprotkan larutan sabun organik untuk mengurangi populasi tungau'),
         TaskShow(title='Bersihkan alat berkebun setelah digunakan')],
        [TaskShow(title='Dokumentasikan populasi tungau dan tindakan lanjutan'),
         TaskShow(title='Evaluasi efektivitas tindakan pengendalian')]
                       ]
                case penyakitEnum.target_spot:
                  return [
                       [TaskShow(title='Potong daun atau bagian tanaman dengan lesi coklat gelap'),
         TaskShow(title='Lakukan sanitasi area sekitar tanaman')],
        [TaskShow(title='Semprotkan fungisida berbasis tembaga pada daun yang tersisa'),
         TaskShow(title='Pantau daun baru untuk gejala tambahan')],
        [TaskShow(title='Pastikan jarak antar tanaman cukup untuk sirkulasi udara yang baik'),
         TaskShow(title='Lakukan inspeksi menyeluruh setiap pagi')],
        [TaskShow(title='Bersihkan gulma di sekitar tanaman'),
         TaskShow(title='Semprotkan ulang fungisida jika gejala bertambah')],
        [TaskShow(title='Gunakan larutan baking soda sebagai tambahan untuk mencegah spora jamur'),
         TaskShow(title='Pantau kondisi tanah untuk menghindari kelembapan berlebih')],
        [TaskShow(title='Gunakan pupuk fosfor untuk memperkuat daya tahan tanaman'),
         TaskShow(title='Sterilkan alat berkebun setelah digunakan')],
        [TaskShow(title='Lakukan dokumentasi mingguan gejala dan evaluasi tindakan'),
         TaskShow(title='Rencanakan tindakan pencegahan untuk minggu berikutnya')]
                       ]
                case penyakitEnum.tomato_yellow_leaf_curl_virus:
                  return [
                       [TaskShow(title='Buang daun yang memiliki bercak hitam kecil'),
         TaskShow(title='Buang tanaman yang menunjukkan gejala parah')],
        [TaskShow(title='Semprotkan neem oil untuk mengontrol kutu putih'),
         TaskShow(title='Pasang perangkap kuning untuk mengurangi populasi kutu putih')],
        [TaskShow(title='Pantau gejala baru pada tanaman sehat'),
         TaskShow(title='Lakukan pemupukan ringan dengan pupuk fosfor dan kalium')],
        [TaskShow(title='Semprotkan neem oil ulang jika kutu putih masih ada'),
         TaskShow(title='Sterilkan alat berkebun setelah digunakan')],
        [TaskShow(title='Gunakan insektisida nabati tambahan untuk populasi kutu putih yang tinggi'),
         TaskShow(title='Pantau tanaman setiap pagi dan sore')],
        [TaskShow(title='Semprotkan larutan sabun organik untuk mencegah penyebaran kutu putih'),
         TaskShow(title='Bersihkan area sekitar tanaman')],
        [TaskShow(title='Dokumentasikan hasil inspeksi mingguan'),
         TaskShow(title='Evaluasi efektivitas kontrol hama dan perbaiki strategi')]
                       ]
                case penyakitEnum.tomato_mosaic_virus:
                  return [
                        [TaskShow(title='Inspeksi seluruh tanaman untuk menemukan gejala mosaik atau daun melintir'),
         TaskShow(title='Buang tanaman yang terinfeksi berat')],
        [TaskShow(title='Sterilkan semua alat berkebun untuk mencegah penyebaran virus'),
         TaskShow(title='Lakukan rotasi tanaman jika memungkinkan')],
        [TaskShow(title='Semprotkan insektisida untuk mengontrol hama pembawa virus (kutu daun)'),
         TaskShow(title='Pantau gejala tambahan pada tanaman sehat')],
        [TaskShow(title='Terapkan pupuk organik untuk memperkuat daya tahan tanaman'),
         TaskShow(title='Lakukan sanitasi area tanaman')],
        [TaskShow(title='Gunakan larutan air dan susu (1:1) untuk menyemprot daun yang menunjukkan gejala ringan'),
         TaskShow(title='Pastikan tanah memiliki kandungan hara cukup')],
        [TaskShow(title='Lakukan pengawasan lanjutan terhadap tanaman dengan gejala ringan'),
         TaskShow(title='Sterilkan alat berkebun setelah digunakan')],
        [TaskShow(title='Dokumentasikan hasil inspeksi mingguan dan tindakan yang dilakukan'),
         TaskShow(title='Diskusikan langkah lanjutan dengan ahli jika gejala tetap ada')]
                       ]
             
    def insert_task(self,tasks:list[list[TaskShow]],plant_id:int):
        tanggal = date.today()
        dates = [tanggal + timedelta(days=i) for i in range(8)]
        task = []
        for tanggal,tugas in zip(dates,tasks):
            for tugas_day in tugas:
                tugas_day = TaskCreate(**tugas_day.dict(),plant_id=plant_id,tanggal=tanggal)
                task.append(self._task_repository.create(tugas_day))
        return task

    def create_task(self, penyakit:penyakitEnum , plant_id:int) -> list[list[TaskShow]]:
    # id plant
        try:
            tasks = self.get_list(penyakit)
            task = self.insert_task(tasks=tasks,plant_id=plant_id)
        except Exception as e:
            raise e
        return task
    
    def get_task_by_plant(self,plant_id:int)->list[TaskShow]:
        # rombak 
        try:
            task = self._task_repository.getByPlant(plant_id)
            if not task:
                raise HTTPException(status_code= 404,detail="Task Not Found")
        except Exception as e:
            raise e
        return task
    
    def show_task(self, task_id: int) -> TaskShow:
        try:
            task = self._task_repository.show(task_id)
            if not task:
                raise HTTPException(status_code= 404,detail="Task Not Found")
        except Exception as e:
            raise e 
        return task
    
    def update_task(self,  data: TaskUpdate,task_id: int):
        try:
            
            plant = self.session.get(Plants,task_id)
            if(plant.user_id != self.user.id):
                raise HTTPException(status_code=404, detail="ID not found")
            task = self._task_repository.update(data,data.id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
        except Exception as e:
            raise e
        return task
    
    def delete_task(self, task_id: int) -> TaskShow:
        try:
            task = self._task_repository.delete(task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
        except Exception as e:
            raise e
        return task
    
  



    
        