#Now that all our models, schemas and controllers have been created, we can put the 
#application together in main.py For all the code chunks mentioned in this step, add them here

#import FastApi and SqlAchelmy dependencies as well as the classes created
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# from . import controllers, models, schemas
from . import controllers, models, schemas
from .database import SessionLocal, engine

#create all tables defined in models.py
models.Base.metadata.create_all(bind=engine)

#create the FastAPI application
app = FastAPI()

#this helper function checks if the database is up
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#these are the endpoints utilising the functions created in the controllers.py 

#this endpoint reads all items created in the db
@app.get("/items", response_model=list[schemas.Item])
def read_items(skip:int=0, limit: int=100, db: Session= Depends(get_db)):
    items = controllers.get_items(db, skip=skip, limit=limit)
    return items

#this enpoint reads an item using the id specified
@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id:int, db: Session= Depends(get_db)):
    db_item= controllers.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

#allows users to create items or add rows to the table
#it expects a Json request body that is validated by our ItemCreate schema
@app.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return controllers.create_item(db=db, item=item)

#Allows users to specify the Id of the item they would like to update in the Url eg./items/1
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = controllers.update_item(db, item_id= item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

#Allows users to delete item by the specified id
@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = controllers.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


