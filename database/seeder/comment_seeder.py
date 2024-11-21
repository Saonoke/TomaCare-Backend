from model import Comments
from sqlmodel import Session, select


class CommentsSeeder:

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def create_comments():
        comments = [
            Comments(
                id=1,
                user_id= 1,
                post_id= 1,
                commentary ="This is a comment"
            ),Comments(
                id=2,
                user_id= 2,
                post_id= 1,
                commentary ="Awesome"
            ),Comments(
                id=3,
                user_id= 2,
                post_id= 2,
                commentary ="Good Job"
            ),
            Comments(
                id=4,
                user_id= 3,
                post_id= 2,
                commentary ="This is a comment"
            ),
            Comments(
                id=5,
                user_id= 1,
                post_id= 3,
                commentary ="This is a comment"
            ),
            Comments(
                id= 6,
                user_id= 3,
                post_id= 3,
                commentary ="Good Job"
            ),
            Comments(
                id=7,
                user_id= 2,
                post_id= 4,
                commentary ="This is a comment"
            ),
        ]

        return comments

    def clear(self):
        comments = self.session.exec(select(Comments)).all()

        for comment in comments :
            self.session.delete(comment)
        self.session.commit()

    def execute(self):
        comments = self.create_comments()
        for comment in comments:
            self.session.add(comment)
        self.session.commit()
