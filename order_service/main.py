from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import orders
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user

app = FastAPI(
    title="Order Service",
    description="Order management service",
    version="1.0.0",
    root_path="/api/order/"
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
    return {"status": "healthy", "service": "order-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Order Service", "version": "1.0.0"}


@app.post("/orders/")
def create_orders(Order: orders, session: Session=Depends(get_session)):
    session.add(Order)
    session.commit()
    session.refresh(Order)
    return Order


@app.get("/orders/")
def get_all_orders(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
):
    return session.exec(select(orders)).all()


@app.get("/orders/{order_id}")
def get_orders_by_id(order_id: int, session: Session=Depends(get_session)):
    Order=session.get(orders, order_id)
    return Order


@app.delete("/orders/", status_code=204)
def delete_orders(session: Session=Depends(get_session)):
    Order=session.exec(select(orders)).all()
    for O in Order:
        session.delete(O)
        session.commit()
    return {"detail": "all orders deleted"}


@app.delete("/orders/{order_id}", status_code=204)
def delete_orders_by_id(order_id: int, session: Session=Depends(get_session)):
    Order=session.get(orders, order_id)
    if not Order:
        raise  HTTPException(status_code=404, detail="order not found")
    session.delete(Order)
    session.commit()
    return{"detail": f"order {order_id}deleted"} 
     

@app.put("/orders/")
def update_orders(data: orders, session: Session=Depends(get_session)):
    Order=session.exec(select(orders)).all()
    if not Order:
        raise HTTPException(status_code=404, detail="order not found")
    update_data=data.dict(exclude_unset=True)
    for O in Order:
        for key, value in update_data.items():
            setattr(O, key, value)
            session.commit()
            for O in Order:
                session.refresh(O)
                return O
            

@app.put("/orders/{order_id}")
def update_orders_by_id(order_id: int, data: orders, session: Session=Depends(get_session)):
  Order=session.get(orders, order_id)
  if not Order:
    raise HTTPException(status_code=404, detail="order not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(Order, key, value)
  session.commit()
  session.refresh(Order)
  return Order 