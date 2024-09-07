#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# cython: language_level=3
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

from fastapi_exts import AppExt

app = FastAPI()
AppExt(app)


class Item(BaseModel):
    user: str
    item: str


@app.get("/")
async def root(data: Annotated[Item, Form()]):
    print(data)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
