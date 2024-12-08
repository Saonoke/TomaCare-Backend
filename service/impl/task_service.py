from fastapi import HTTPException
from sqlmodel import Session
from database.repository import TaskRepositoryMeta, TaskRepository
from database.schema import TaskBase, TaskCreate, TaskShow, TaskUpdate
from service import TaskServiceMeta
from enumeration import penyakitEnum
from datetime import date, timedelta


    



class TaskService(TaskServiceMeta):
    def __init__(self,session:Session) :
        self.session = session
        self._task_repository : TaskRepositoryMeta = TaskRepository(self.session)

    def get_list(self,penyakit:penyakitEnum)-> list[TaskShow]:
         match penyakit:
                case penyakitEnum.bacterial_spot:
                   return [
                       [TaskShow(title='Buang daun yang memiliki bercak hitam kecil',)],
                       [TaskShow(title='Semprotkan fungisida berbasis tembaga pada daun yang tersisa')],
                       [TaskShow(title='Hindari penyiraman dari atas (gunakan penyiraman langsung ke tanah)')],
                       [TaskShow(title='Pantau perkembangan bercak baru pada buah atau daun')],
                       [TaskShow(title='Semprotkan insektisida alami untuk mengontrol serangga pembawa bakteri')],
                       [TaskShow(title='Lakukan sanitasi area sekitar tanaman')],
                       [TaskShow(title='Dokumentasikan hasil pemantauan dan tindakan yang dilakukan')],
                       ]
                case penyakitEnum.early_blight:
                  return [
                       [TaskShow(title='Buang daun dengan lesi coklat berbentuk lingkaran konsentris',)],
                       [TaskShow(title='Semprotkan fungisida berbasis tembaga pada semua tanaman')],
                       [TaskShow(title='Pastikan tanah tidak kering dan memiliki kelembapan cukup')],
                       [TaskShow(title='Pantau tanaman untuk gejala tambahan')],
                       [TaskShow(title='Gunakan mulsa untuk menjaga kelembapan tanah dan mencegah penyebaran spora')],
                       [TaskShow(title='Semprotkan fungisida ulang jika perlu')],
                       [TaskShow(title='Dokumentasikan hasil inspeksi mingguan')],
                       ]
                case penyakitEnum.late_blight:
                  return [
                       [TaskShow(title='Buang daun atau tanaman yang menunjukkan lesi coklat kehijauan',)],
                       [TaskShow(title='Semprotkan fungisida sistemik pada semua tanaman')],
                       [TaskShow(title='Pastikan drainase tanah baik untuk mencegah genangan air')],
                       [TaskShow(title='Pantau daun baru untuk mendeteksi lesi tambahan')],
                       [TaskShow(title='Lakukan sanitasi area kebun')],
                       [TaskShow(title='Semprotkan fungisida sistemik ulang jika gejala terus menyebar')],
                       [TaskShow(title='Dokumentasikan perubahan gejala pada tanaman')],
                       ]
                case penyakitEnum.leaf_mold:
                  return [
                       [TaskShow(title='Potong daun dengan bercak kuning atau jamur hijau',)],
                       [TaskShow(title='Semprotkan fungisida berbasis sulfur')],
                       [TaskShow(title='Pastikan area tanaman memiliki ventilasi yang baik')],
                       [TaskShow(title='Pantau daun baru untuk gejala tambahan')],
                       [TaskShow(title='Lakukan penyiraman pagi hari untuk mengurangi kelembapan di malam hari')],
                       [TaskShow(title='Semprotkan fungisida berbasis sulfur ulang jika jamur masih ada')],
                       [TaskShow(title='Evaluasi keberhasilan penanganan')],
                       ]
                case penyakitEnum.septorial_leaf_spot:
                  return [
                       [TaskShow(title='Buang daun dengan bercak coklat kecil',)],
                       [TaskShow(title='Semprotkan fungisida berbasis tembaga')],
                       [TaskShow(title='Pastikan jarak antar tanaman cukup')],
                       [TaskShow(title='Pantau perkembangan bercak baru')],
                       [TaskShow(title='Lakukan penyiraman tanpa membasahi daun')],
                       [TaskShow(title='Semprotkan fungisida ulang jika diperlukan')],
                       [TaskShow(title='Dokumentasikan hasil inspeksi mingguan')],
                       ]
                case penyakitEnum.spidermites_two_spottedspider_mite:
                  return [
                       [TaskShow(title='Semprotkan air langsung pada tanaman untuk menghilangkan tungau',)],
                       [TaskShow(title='Semprotkan neem oil atau insektisida alami')],
                       [TaskShow(title='Pantau jaring laba-laba halus di bawah daun')],
                       [TaskShow(title='Semprotkan air ulang jika tungau masih terlihat')],
                       [TaskShow(title='Tambahkan predator alami seperti kumbang ladybug jika memungkinkan')],
                       [TaskShow(title='Semprotkan neem oil ulang jika infestasi masih ada')],
                       [TaskShow(title='Evaluasi populasi tungau dan tindakan lanjutan')],
                       ]
                case penyakitEnum.target_spot:
                  return [
                       [TaskShow(title='Potong daun atau bagian tanaman yang memiliki lesi coklat gelap',)],
                       [TaskShow(title='Semprotkan fungisida berbasis tembaga pada daun yang tersisa')],
                       [TaskShow(title='Pastikan jarak antar tanaman cukup untuk sirkulasi udara yang baik')],
                       [TaskShow(title='Pantau daun baru untuk mencegah penyebaran')],
                       [TaskShow(title='Bersihkan gulma di sekitar tanaman')],
                       [TaskShow(title='Semprotkan ulang fungisida jika diperlukan')],
                       [TaskShow(title='Lakukan dokumentasi dan evaluasi efektivitas fungisida')],
                       ]
                case penyakitEnum.tomato_yellow_leaf_curl_virus:
                  return [
                       [TaskShow(title='Buang daun yang memiliki bercak hitam kecil'), TaskShow(title='Buang tanaman yang menunjukkan gejala parah',)],
                       [TaskShow(title='Semprotkan neem oil untuk mengontrol kutu putih')],
                       [TaskShow(title='Pasang perangkap kuning untuk mengurangi populasi kutu putih')],
                       [TaskShow(title='Pantau gejala baru pada tanaman sehat')],
                       [TaskShow(title='Lakukan pemupukan ringan dengan pupuk fosfor dan kalium')],
                       [TaskShow(title='Semprotkan neem oil ulang jika kutu putih masih ada')],
                       [TaskShow(title='Evaluasi efektivitas kontrol hama')],
                       ]
                case penyakitEnum.tomato_mosaic_virus:
                  return [
                        [TaskShow(title='Inspeksi seluruh tanaman untuk menemukan gejala mosaik atau daun melintir.'), TaskShow(title='Buang tanaman yang terinfeksi berat',)],
                        [TaskShow(title='Sterilkan semua alat berkebun untuk mencegah penyebaran virus'), TaskShow(title='Lakukan rotasi tanaman jika memungkinkan',)],
                       [TaskShow(title='Semprotkan insektisida untuk mengontrol hama pembawa virus (kutu daun)')],
                       [TaskShow(title='Pantau gejala tambahan pada tanaman sehat')],
                       [TaskShow(title='Terapkan pupuk organik untuk memperkuat daya tahan tanaman')],
                       [TaskShow(title='Lakukan pengawasan lanjutan terhadap tanaman dengan gejala ringan')],
                       [TaskShow(title='Dokumentasikan hasil inspeksi dan catat tanaman yang masih menunjukkan gejala')],
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
            print(data)
            task = self._task_repository.update(data,task_id)
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
    
  



    
        