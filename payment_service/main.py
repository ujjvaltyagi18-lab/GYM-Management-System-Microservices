from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import payment
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user

app = FastAPI(
    title="Payment Service",
    description="Payment management service",
    version="1.0.0",
    root_path="/api/payment/"
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
    return {"status": "healthy", "service": "payment-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Payment Service", "version": "1.0.0"}


@app.post("/payments/")
def create_payments(Payment: payment, session: Session=Depends(get_session)):
    session.add(Payment)
    session.commit()
    session.refresh(Payment)
    return Payment


@app.get("/payments/")
def get_all_payments(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
):
    return session.exec(select(payment)).all()


@app.get("/payments/{payment_id}")
def get_payments_by_id(payment_id: int, session: Session=Depends(get_session)):
    Payment=session.get(payment, payment_id)
    return Payment


@app.delete("/payments/", status_code=204)
def delete_payments(session: Session=Depends(get_session)):
    Payment=session.exec(select(payment)).all()
    for P in Payment:
        session.delete(P)
        session.commit()
    return {"detail": "all payments deleted"}

 
@app.delete("/payments/{payment_id}", status_code=204)
def delete_payments_by_id(payment_id: int, session: Session=Depends(get_session)):
    Payment=session.get(payment, payment_id)
    if not Payment:
        raise  HTTPException(status_code=404, detail="payment not found")
    session.delete(Payment)
    session.commit()
    return{"detail": f"payment {payment_id}deleted"} 
     

@app.put("/payments/")
def update_payments(data: payment, session: Session=Depends(get_session)):
    Payment=session.exec(select(payment)).all()
    if not Payment:
        raise HTTPException(status_code=404, detail="payment not found")
    update_data=data.dict(exclude_unset=True)
    for P in Payment:
        for key, value in update_data.items():
            setattr(P, key, value)
            session.commit()
            for P in Payment:
                session.refresh(P)
                return P
            

@app.put("/payments/{payment_id}")
def update_payments_by_id(payment_id: int, data: payment, session: Session=Depends(get_session)):
  Payment=session.get(payment, payment_id)
  if not Payment:
    raise HTTPException(status_code=404, detail="payment not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(Payment, key, value)
  session.commit()
  session.refresh(Payment)
  return Payment 