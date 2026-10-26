from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import equipments, products
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user


app = FastAPI(
    title="Inventory Service",
    description="Inventory management service",
    version="1.0.0",
    root_path="/api/inventory/"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "inventory-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Inventory Service", "version": "1.0.0"}


@app.post("/equipments/")
def create_equipments(Equipment: equipments, session: Session=Depends(get_session)):
    session.add(Equipment)
    session.commit()
    session.refresh(Equipment)
    return Equipment


@app.get("/equipments/")
def get_all_equipments(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
    ):
    return session.exec(select(equipments)).all()


@app.get("/equipments/{equipment_id}")
def get_equipments_by_id(equipment_id: int, session: Session=Depends(get_session)):
    Equipment=session.get(equipments, equipment_id)
    return Equipment


@app.delete("/equipments/", status_code=204)
def delete_equipments(session: Session=Depends(get_session)):
    Equipment=session.exec(select(equipments)).all()
    for E in Equipment:
        session.delete(E)
        session.commit()
    return {"detail": "all equipments deleted"}


@app.delete("/equipments/{equipment_id}", status_code=204)
def delete_equipments_by_id(equipment_id: int, session: Session=Depends(get_session)):
    Equipment=session.get(equipments, equipment_id)
    if not Equipment:
        raise  HTTPException(status_code=404, detail="equipment not found")
    session.delete(Equipment)
    session.commit()
    return{"detail": f"equipment {equipment_id}deleted"} 
     

@app.put("/equipments/")
def update_equipments(data: equipments, session: Session=Depends(get_session)):
    Equipment=session.exec(select(equipments)).all()
    if not Equipment:
        raise HTTPException(status_code=404, detail="equipment not found")
    update_data=data.dict(exclude_unset=True)
    for E in Equipment:
        for key, value in update_data.items():
            setattr(E, key, value)
            session.commit()
            for E in Equipment:
                session.refresh(E)
                return E
            

@app.put("/equipments/{equipment_id}")
def update_equipments_by_id(equipment_id: int, data: equipments, session: Session=Depends(get_session)):
  Equipment=session.get(equipments, equipment_id)
  if not Equipment:
    raise HTTPException(status_code=404, detail="equipment not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(Equipment, key, value)
  session.commit()
  session.refresh(Equipment)
  return Equipment         




@app.post("/products/")
def create_products(Products: products, session: Session=Depends(get_session)):
    session.add(Products)
    session.commit()
    session.refresh(Products)
    return Products


@app.get("/products/")
def get_all_products(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
):
    return session.exec(select(products)).all()


@app.get("/products/{product_id}")
def get_products_by_id(product_id: int, session: Session=Depends(get_session)):
    Products=session.get(products, product_id)
    return Products


@app.delete("/products/", status_code=204)
def delete_products(session: Session=Depends(get_session)):
    Products=session.exec(select(products)).all()
    for P in Products:
        session.delete(P)
        session.commit()
    return {"detail": "all products deleted"}


@app.delete("/products/{product_id}", status_code=204)
def delete_products_by_id(product_id: int, session: Session=Depends(get_session)):
    Products=session.get(products, product_id)
    if not Products:
        raise  HTTPException(status_code=404, detail="product not found")
    session.delete(Products)
    session.commit()
    return{"detail": f"product {product_id}deleted"} 
     

@app.put("/products/")
def update_products(data: products, session: Session=Depends(get_session)):
    Products=session.exec(select(products)).all()
    if not Products:
        raise HTTPException(status_code=404, detail="product not found")
    update_data=data.dict(exclude_unset=True)
    for P in Products:
        for key, value in update_data.items():
            setattr(P, key, value)
            session.commit()
            for P in Products:
                session.refresh(P)
                return P
            

@app.put("/products/{product_id}")
def update_products_by_id(product_id: int, data: products, session: Session=Depends(get_session)):
    Products=session.get(products, product_id)
    if not Products:
        raise HTTPException(status_code=404, detail="product not found")
    for key, value in data.dict(exclude_unset=True):
        setattr(Products, key, value)
    session.commit()
    session.refresh(Products)
    return Products

                