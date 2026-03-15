from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import uuid

# In-memory database
items_db = {}

app = FastAPI(title="Item Service", description="CRUD Operations for Items")
security = HTTPBearer()

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class Item(ItemCreate):
    id: str

# Very simple token validation (in a real app, verify JWT signature from Auth Service)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token format")
    # Here we simulate validation (e.g. check if token is "mock_id_token" or decode real JWT)
    if token == "invalid":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.get("/items", response_model=List[Item], tags=["Items"])
def get_items(token: str = Depends(verify_token)):
    return list(items_db.values())

@app.post("/items", response_model=Item, tags=["Items"])
def create_item(item: ItemCreate, token: str = Depends(verify_token)):
    item_id = str(uuid.uuid4())
    new_item = Item(id=item_id, **item.model_dump())
    items_db[item_id] = new_item
    return new_item

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(item_id: str, token: str = Depends(verify_token)):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item(item_id: str, item_update: ItemCreate, token: str = Depends(verify_token)):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = Item(id=item_id, **item_update.model_dump())
    items_db[item_id] = updated_item
    return updated_item

@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: str, token: str = Depends(verify_token)):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"detail": "Item deleted"}

# CORS setup for development
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
