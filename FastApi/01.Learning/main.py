from enum import Enum
from typing import Annotated, Literal

from fastapi import FastAPI, Query, Path, Body, Cookie
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    description: str | None = None


class ModelName(str, Enum):
    joel = "joel"
    dark = "dark"
    dr11 = "dr11"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/now")
async def item_now():
    return {"message": "The current item"}


@app.get("/items/{item_id}")
async def item(item_id: Annotated[int | None, Path(title="Item id of product", description="Hehe")]):
    return {"message": item_id}


@app.post("/items/add")
async def insert_item(item: Item):
    item.name = item.name.upper()
    return item


@app.get("/items")
async def items_me():
    return ["Ship", "Lorry"]


@app.get("/items")
async def items():
    return ["Car", "Bike", "Boat"]


@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.dark:
        return {"message": f'This is {model_name}'}
    elif model_name.value == "joel":
        return {'message': f'This is {model_name.value}'}
    return model_name


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/query")
async def get_query(skip: int = 0, limit: int = 10):
    return {"message": "Query success", "skip": skip, "limit": limit}


@app.get("/queries/")
async def get_query(q: Annotated[str | None, Query(max_length=2)] = None):
    return {"message": q}


@app.get("/lists/")
async def get_list(q: Annotated[
    list[int] | None,
    Query(
        alias="query",
        title="List Api use",
        description="This api is for showing Query Parameter as list",
        deprecated=True
    )
] = None):
    return {"message": q}


''' Query Parameter Model'''


class QueryParamModel(BaseModel):
    limit: int = Field(default=..., gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal['created_on', 'updated_on'] = 'created_on'
    tags: list[str] = list()


@app.get("/query/model")
# If Annotated and Query is not given it'll become request body
async def get_query_param_model(filter_query: Annotated[QueryParamModel, Query()]):
    return filter_query


@app.post("/body")
async def multiple_req_body(item: Item, model: Annotated[ModelName, Body()], id: Annotated[int, Body()]):
    op: dict = {
        'id': id,
        'item': item,
        'model': model
    }
    return op


@app.post("/single")
async def post_single_body_embedd(id: Annotated[QueryParamModel, Body(embed=True)]):
    return id


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights


class Items(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@app.put("/itemsd/{item_id}")
async def update_item(item_id: int, item: Items):
    results = {"item_id": item_id, "item": item}
    return results


@app.get("/cookie")
async def get_cookie(ads_id: Annotated[str, Cookie()]):
    return ads_id
