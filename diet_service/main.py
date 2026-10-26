from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import diet
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user



app = FastAPI(
    title="Diet Service",
    description="Diet management service",
    version="1.0.0",
    root_path="/api/diet"
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
    return {"status": "healthy", "service": "diet-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Diet Service", "version": "1.0.0"}


@app.post("/diet/")
def create_diet(Diet: diet, session: Session=Depends(get_session)):
    session.add(Diet)
    session.commit()
    session.refresh(Diet)
    return Diet


@app.get("/diet/")
def get_all_diet(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return session.exec(select(diet)).all()


@app.get("/diet/{diet_id}")
def get_diet_by_id(diet_id: int, session: Session=Depends(get_session)):
    Diet=session.get(diet, diet_id)
    return Diet


@app.delete("/diet/", status_code=204)
def delete_diet(session: Session=Depends(get_session)):
    Diet=session.exec(select(diet)).all()
    for D in Diet:
        session.delete(D)
        session.commit()
    return {"detail": "all diets deleted"}


@app.delete("/diet/{diet_id}", status_code=204)
def delete_diet_by_id(diet_id: int, session: Session=Depends(get_session)):
    Diet=session.get(diet, diet_id)
    if not Diet:
        raise  HTTPException(status_code=404, detail="diet not found")
    session.delete(Diet)
    session.commit()
    return{"detail": f"diet {diet_id}deleted"} 
     

@app.put("/diet/")
def update_diet(data: diet, session: Session=Depends(get_session)):
    Diet=session.exec(select(diet)).all()
    if not Diet:
        raise HTTPException(status_code=404, detail="diet not found")
    update_data=data.dict(exclude_unset=True)
    for D in Diet:
        for key, value in update_data.items():
            setattr(D, key, value)
            session.commit()
            for D in Diet:
                session.refresh(D)
                return D
            

@app.put("/diet/{diet_id}")
def update_diet_by_id(diet_id: int, data: diet, session: Session=Depends(get_session)):
  Diet=session.get(diet, diet_id)
  if not Diet:
    raise HTTPException(status_code=404, detail="diet not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(Diet, key, value)
  session.commit()
  session.refresh(Diet)
  return Diet            

    
                