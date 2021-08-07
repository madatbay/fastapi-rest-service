from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.fields import Field


class Item(BaseModel):
    name: str
    describtion: Optional[str] = Field(None, max_length=300)
    price: float = Field(..., gt=0)
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "FastAPI"}


@app.get("/item/{item_name}")
async def get_item(item_name: str):
    return {"item_name": item_name}


@app.post("/item/create")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/item/put/{item_id}")
async def put_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
