from pydantic import BaseModel, Field
from datetime import datetime

current_year = datetime.now().year

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    year: int = Field(..., ge=1500, le=current_year)  

class BookCreate(BookBase):
    pass
class Book(BookBase):
    id: int

    class Config:
        from_attribute = True
    