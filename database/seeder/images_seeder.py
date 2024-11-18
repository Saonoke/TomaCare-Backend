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
                image_path='blah',
                public_id=111
            ),Images(
                id=2,
                image_path='blahblah',
                public_id=222
            ),Images(
                id=3,
                image_path='blahblahblah',
                public_id=333
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
