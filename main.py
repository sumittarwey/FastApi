# from typing import Union
from fastapi import Depends, FastAPI, HTTPException
import models
from fastapi import FastAPI
import schema as schemas
from database import engine,get_db
from repositories import ItemRepo, StoreRepo,UserRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from auth_bearer import JWTBearer,signJWT



app = FastAPI(title="Sample FastAPI Application",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version="1.0.0",)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


@app.post('/items', tags=["Item"],dependencies=[Depends(JWTBearer())],response_model=schemas.Item,status_code=201)
async def create_item(item_request: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create an Item and store it in the database
    """
    
    db_item = ItemRepo.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists!")

    return await ItemRepo.create(db=db, item=item_request)

@app.get('/items', tags=["Item"],dependencies=[Depends(JWTBearer())],response_model=List[schemas.Item])
def get_all_items(name: Optional[str] = None,db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """
    if name:
        items =[]
        db_item = ItemRepo.fetch_by_name(db,name)
        items.append(db_item)
        return items
    else:
        return ItemRepo.fetch_all(db)


@app.get('/items/{item_id}',dependencies=[Depends(JWTBearer())], tags=["Item"],response_model=schemas.Item)
def get_item(item_id: int,db: Session = Depends(get_db)):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db,item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item

@app.delete('/items/{item_id}',dependencies=[Depends(JWTBearer())], tags=["Item"])
async def delete_item(item_id: int,db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db,item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await ItemRepo.delete(db,item_id)
    return "Item deleted successfully!"

@app.put('/items/{item_id}',dependencies=[Depends(JWTBearer())], tags=["Item"],response_model=schemas.Item)
async def update_item(item_id: int,item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an Item stored in the database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.name = update_item_encoded['name']
        db_item.price = update_item_encoded['price']
        db_item.description = update_item_encoded['description']
        db_item.store_id = update_item_encoded['store_id']
        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")
    
    
@app.post('/stores', tags=["Store"],dependencies=[Depends(JWTBearer())],response_model=schemas.Store,status_code=201)
async def create_store(store_request: schemas.StoreCreate, db: Session = Depends(get_db)):
    """
    Create a Store and save it in the database
    """
    db_store = StoreRepo.fetch_by_name(db, name=store_request.name)
    if db_store:
        raise HTTPException(status_code=400, detail="Store already exists!")

    return await StoreRepo.create(db=db, store=store_request)

@app.get('/stores', tags=["Store"],dependencies=[Depends(JWTBearer())],response_model=List[schemas.Store])
def get_all_stores(name: Optional[str] = None,db: Session = Depends(get_db)):
    """
    Get all the Stores stored in database
    """
    if name:
        stores =[]
        db_store = StoreRepo.fetch_by_name(db,name)
        stores.append(db_store)
        return stores
    else:
        return StoreRepo.fetch_all(db)
    
@app.get('/stores/{store_id}',dependencies=[Depends(JWTBearer())], tags=["Store"],response_model=schemas.Store)
def get_store(store_id: int,db: Session = Depends(get_db)):
    """
    Get the Store with the given ID provided by User stored in database
    """
    db_store = StoreRepo.fetch_by_id(db,store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found with the given ID")
    return db_store

@app.delete('/stores/{store_id}',dependencies=[Depends(JWTBearer())], tags=["Store"])
async def delete_store(store_id: int,db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_store = StoreRepo.fetch_by_id(db,store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found with the given ID")
    await StoreRepo.delete(db,store_id)
    return "Store deleted successfully!"

@app.post('/create-user/',tags=['User'])
async def create_user(user:schemas.UserSchema,db:Session = Depends(get_db)):
    await UserRepo.create(db,user)
    return "User Inserted successfully!"


@app.get('/user/',dependencies=[Depends(JWTBearer())],tags=['User'])
async def get_user(db:Session = Depends(get_db)):
    alluser=await UserRepo.getAllUser(db)
    return alluser

@app.get('/user/{user_id}',dependencies=[Depends(JWTBearer())],tags=['User'])
async def get_user(user_id:int,db:Session = Depends(get_db)):
    user=await UserRepo.fetch_user_by_id(user_id,db)
    return user

@app.post('/login/',tags=['user'])
async def get_user(login:schemas.UserLoginSchema,db:Session = Depends(get_db)):
    login=await UserRepo.login(db,login)
    print(login.id)
    if login:
        return signJWT(login.id)
    return "Invalid login"

    

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)