from model import Reaction
from sqlmodel import Session, select

from model.reaction_model import ReactionEnum


class ReactionSeeder:

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def create_reactions():
        reactions = [
            Reaction(
                posts_id=1,
                users_id=1,
                reaction_type=ReactionEnum.LIKE.value
            ),
            Reaction(
                posts_id=1,
                users_id=2,
                reaction_type=ReactionEnum.DISLIKE.value
            ),
            Reaction(
                posts_id=2,
                users_id=1,
                reaction_type=ReactionEnum.LIKE.value
            ),
            Reaction(
                posts_id=2,
                users_id=3,
                reaction_type=ReactionEnum.DISLIKE.value
            ),
            Reaction(
                posts_id=3,
                users_id=1,
                reaction_type=ReactionEnum.LIKE.value
            ),
            Reaction(
                posts_id=3,
                users_id=2,
                reaction_type=ReactionEnum.LIKE.value
            ),
            Reaction(
                posts_id=4,
                users_id=3,
                reaction_type=ReactionEnum.DISLIKE.value
            ),
            Reaction(
                posts_id=5,
                users_id=2,
                reaction_type=ReactionEnum.LIKE.value
            ),
            Reaction(
                posts_id=5,
                users_id=3,
                reaction_type=ReactionEnum.LIKE.value
            )
        ]

        return reactions

    def clear(self):
        reactions = self.session.exec(select(Reaction)).all()

        for reaction in reactions :
            self.session.delete(reaction)
        self.session.commit()

    def execute(self):
        reactions = self.create_reactions()
        for reaction in reactions:
            self.session.add(reaction)
        self.session.commit()












