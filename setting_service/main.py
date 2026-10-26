from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import setting
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user

app = FastAPI(
    title="Setting Service",
    description="Setting management service",
    version="1.0.0",
    root_path="/api/setting/"
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
    return {"status": "healthy", "service": "setting-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Setting Service", "version": "1.0.0"}


@app.post("/settings/")
def create_setting(Setting: setting, session: Session=Depends(get_session)):
    session.add(Setting)
    session.commit()
    session.refresh(Setting)
    return Setting


@app.get("/settings/")
def get_all_settings(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
):
    return session.exec(select(setting)).all()


@app.get("/settings/{setting_id}")
def get_setting_by_id(setting_id: int, session: Session=Depends(get_session)):
    Setting=session.get(setting, setting_id)
    return Setting


@app.delete("/settings/", status_code=204)
def delete_settings(session: Session=Depends(get_session)):
    Settings=session.exec(select(setting)).all()
    for S in Settings:
        session.delete(S)
        session.commit()
    return {"detail": "all settings deleted"}

 
@app.delete("/settings/{setting_id}", status_code=204)
def delete_setting_by_id(setting_id: int, session: Session=Depends(get_session)):
    Setting=session.get(setting, setting_id)
    if not Setting:
        raise  HTTPException(status_code=404, detail="setting not found")
    session.delete(Setting)
    session.commit()
    return{"detail": f"setting {setting_id}deleted"} 
     

@app.put("/settings/")
def update_setting(data: setting, session: Session=Depends(get_session)):
    Settings=session.exec(select(setting)).all()
    if not Settings:
        raise HTTPException(status_code=404, detail="setting not found")
    update_data=data.dict(exclude_unset=True)
    for S in Settings:
        for key, value in update_data.items():
            setattr(S, key, value)
            session.commit()
            for S in Settings:
                session.refresh(S)
                return S
            

@app.put("/settings/{setting_id}")
def update_setting_by_id(setting_id: int, data: setting, session: Session=Depends(get_session)):
  Setting=session.get(setting, setting_id)
  if not Setting:
    raise HTTPException(status_code=404, detail="setting not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(Setting, key, value)
  session.commit()
  session.refresh(Setting)
  return Setting 