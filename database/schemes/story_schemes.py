from pydantic import BaseModel


class StoryBase(BaseModel):
    title: str


class StoryCreate(StoryBase):
    pass


class StoryUpdate(StoryBase):
    pass


class StoryUpdatePartial(StoryBase):
    title: str | None = None


class Story(StoryBase):
    id: int