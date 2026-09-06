from datetime import datetime

from pydantic import BaseModel, Field


class BlogInput(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., max_length=100)
    constent: str = Field(..., min_length=2, max_length=400)
    image_loc: str = Field(None, max_length=400)


class Blog(BlogInput):
    id: int
    modified_dt: datetime
