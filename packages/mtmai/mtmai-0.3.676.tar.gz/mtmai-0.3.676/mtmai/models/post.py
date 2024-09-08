from datetime import datetime

from sqlmodel import Field, SQLModel

from mtmai.mtlibs import mtutils


class PostTabBase(SQLModel):
    name: str | None = Field(default=None)


class PostTab(PostTabBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)


# # Database model, database table inferred from class name
# class Post(PostBase, table=True):
#     id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)


class PostContent(SQLModel, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    # post_id: str | None = Field(default=None, foreign_key="blogpost.id")
    # post: "BlogPost" = Relationship(back_populates="content")


class PostBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    content: str | None = Field(default=None)


class Post(PostBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    content_id: str | None = Field(default=None, foreign_key="postcontent.id")
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
