from pydantic import BaseModel


class PageBase(BaseModel):
    page_text: str


class PageCreate(PageBase):
    pass


class PageUpdate(PageBase):
    pass


class PageUpdatePartial(PageBase):
    page_text: str | None = None


class Page(PageBase):
    id: int