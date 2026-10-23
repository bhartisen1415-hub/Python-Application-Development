from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status

from app import database
from app.auth import verify_api_key
from app.schemas import ItemCreate, ItemResponse, ItemUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(
    title="Python Application Development API",
    description="A REST API using FastAPI and SQLite with CRUD operations.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {"message": "Python Application Development API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_item(item: ItemCreate):
    return database.create_item(item.name, item.description, item.price)


@app.get(
    "/items",
    response_model=list[ItemResponse],
    dependencies=[Depends(verify_api_key)],
)
def list_items():
    return database.get_all_items()


@app.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    dependencies=[Depends(verify_api_key)],
)
def read_item(item_id: int):
    item = database.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    dependencies=[Depends(verify_api_key)],
)
def update_item(item_id: int, item: ItemUpdate):
    updated = database.update_item(item_id, item.name, item.description, item.price)
    if updated is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@app.delete("/items/{item_id}", dependencies=[Depends(verify_api_key)])
def remove_item(item_id: int):
    if not database.delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
