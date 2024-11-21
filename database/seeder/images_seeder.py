from model import Images
from sqlmodel import Session, select


class ImagesSeeder:

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def create_images():
        images = [
            Images(
                id=1,
                image_path='https://www.infarm.co.id/uploads/article/Mf8PKypnlq3oEEQAhwFHhoOhRDAX2HNvGNMllmv8.jpg',
                public_id=111
            ),Images(
                id=2,
                image_path='https://asset.kompas.com/crops/pU7iqS4RZMviTem5OgqDCm9Q-fg=/1x0:1000x666/1200x800/data/photo/2023/01/23/63ceaa9b917ab.jpg',
                public_id=222
            ),Images(
                id=3,
                image_path='https://gkmdblog.s3.ap-southeast-1.amazonaws.com/wp-content/uploads/2023/12/14235212/Blog-Tanaman-Tomat.jpeg',
                public_id=333
            ),Images(
                id=4,
                image_path='https://imgcdn.stablediffusionweb.com/2024/3/27/374a7884-efc9-4546-b53e-d29d6033e7d9.jpg',
                public_id=444
            ),Images(
                id=5,
                image_path='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSsoEzyJdtks-inuZFrlFLsJ9VUoTa-9O87-A&s',
                public_id=555
            ),Images(
                id=6,
                image_path='https://starryai.com/cdn-cgi/image/format=avif,quality=90/https://cdn.prod.website-files.com/61554cf069663530fc823d21/6369fed004b5b041b7ed686a_download-8-min.png',
                public_id=666
            ),
        ]

        return images

    def clear(self):
        images = self.session.exec(select(Images)).all()

        for image in images :
            self.session.delete(image)
        self.session.commit()

    def execute(self):
        images = self.create_images()
        for image in images:
            self.session.add(image)
        self.session.commit()
