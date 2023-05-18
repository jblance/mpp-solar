from pydantic import BaseModel


class MQTTMessageBase(BaseModel):
    topic: str
    message: str


class MQTTMessageCreate(MQTTMessageBase):
    pass


class MQTTMessage(MQTTMessageBase):
    id: int

    class Config:
        orm_mode = True


# Demo code
class ItemBase(BaseModel):
    title: str
    # description: str | None = None
    description: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
