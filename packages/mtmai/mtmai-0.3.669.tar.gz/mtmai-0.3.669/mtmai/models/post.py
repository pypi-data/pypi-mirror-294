from sqlmodel import Field, SQLModel

from mtmai.mtlibs import mtutils


class PostTabBase(SQLModel):
    name: str | None = Field(default=None)


class PostTab(PostTabBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)


class PostBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    content: str | None = Field(default=None)


# Database model, database table inferred from class name
class Post(PostBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
