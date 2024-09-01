from redis_om import Field, HashModel, Migrator


class PostsCacheModel(HashModel):
    id: int = Field(index=True)
    uuid: str = Field(index=True)
    title: str = Field(index=True)
    content: str
    published: str
    rating: float = Field(index=True)
    created_at: str
    updated_at: str
    deleted_at: str

Migrator().run()