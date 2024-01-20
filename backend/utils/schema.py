from pydantic import BaseModel


class MakeAllOptional(BaseModel):
    def __init__(self, **data):
        super().__init__(**{k: None for k in self.__fields__}, **data)
        for name, field in self.__fields__.items():
            field.required = False
