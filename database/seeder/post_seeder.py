from model import Posts
from sqlmodel import Session, select


class PostSeeder:

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def create_posts():
        posts = [
            Posts(
                id=1,
                title='Cara Mengatasi Penyakit Layu pada Tomat',
                body='Tanaman tomat saya layu, adakah yang punya solusi?',
                user_id=1,
                image_id=1
            ),
            Posts(
                id=2,
                title='Tips Menjaga Kelembaban Tanah',
                body='Saya menggunakan metode mulsa untuk menjaga kelembaban tanah, apakah efektif untuk tomat?',
                user_id=1,
                image_id=1
            ),
            Posts(
                id=3,
                title='Penyakit Bercak Daun',
                body='Tomat saya terkena bercak daun coklat, bagaimana cara mengatasinya?',
                user_id=2,
                image_id=2
            ),
            Posts(
                id=4,
                title='Jenis Pupuk Terbaik untuk Tomat',
                body='Ada rekomendasi pupuk yang baik untuk meningkatkan hasil panen tomat?',
                user_id=2,
                image_id=3
            ),
            Posts(
                id=5,
                title='Waktu Penyiraman yang Tepat',
                body='Kapan waktu yang tepat untuk menyiram tomat agar tidak mudah terkena penyakit?',
                user_id=2,
                image_id=3
            )
        ]

        return posts

    def clear(self):
        posts = self.session.exec(select(Posts)).all()

        for post in posts :
            self.session.delete(post)
        self.session.commit()

    def execute(self):
        posts = self.create_posts()
        for post in posts:
            self.session.add(post)
        self.session.commit()
