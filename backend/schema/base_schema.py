from typing import Optional, Union

from pydantic import BaseModel


class FindBase(BaseModel):
    ordering: Optional[str]
    page: Optional[int]
    page_size: Optional[Union[int, str]]
