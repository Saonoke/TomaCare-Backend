from sqlmodel import Field, SQLModel, Relationship

class Images(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    image_path: str 
    public_id : str | None = Field(default=None)

    user: 'Users' = Relationship(back_populates='profile')
    post: 'Posts' = Relationship(back_populates='image')
    plant: 'Plants' = Relationship(back_populates='image')
