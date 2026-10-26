from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import attendance
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user


app = FastAPI(
    title="Attendance Service",
    description="Attendance management service",
    version="1.0.0",
    root_path="/api/attendance/"
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
    return {"status": "healthy", "service": "attendance-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Attendance Service", "version": "1.0.0"}



@app.post("/attendance/")
def create_attendance(Attendance: attendance, session: Session=Depends(get_session)):
    session.add(Attendance)
    session.commit()
    session.refresh(Attendance)
    return Attendance


@app.get("/attendance/")
def get_all_attendance(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return session.exec(select(attendance)).all()


@app.get("/attendance/{attendance_id}")
def get_attendance_by_id(attendance_id: int, session: Session=Depends(get_session)):
    Attendance=session.get(attendance, attendance_id)
    return Attendance


@app.delete("/attendance/", status_code=204)
def delete_attendance(session: Session=Depends(get_session)):
    Attendance=session.exec(select(attendance)).all()
    for Attend in Attendance:
        session.delete(Attend)
        session.commit()
    return {"detail": "all attendance deleted"}


@app.delete("/attendance/{attendance_id}", status_code=204)
def delete_attendance_by_id(attendance_id: int, session: Session=Depends(get_session)):
    Attendance=session.get(attendance, attendance_id)
    if not Attendance:
        raise  HTTPException(status_code=404, detail="attendance not found")
    session.delete(Attendance)
    session.commit()
    return{"detail": f"attendance {attendance_id}deleted"} 
     

@app.put("/attendance/")
def update_attendance(data: attendance, session: Session=Depends(get_session)):
    Attendance=session.exec(select(attendance)).all()
    if not Attendance:
        raise HTTPException(status_code=404, detail="attendance not found")
    update_data=data.dict(exclude_unset=True)
    for A in Attendance:
        for key, value in update_data.items():
            setattr(A, key, value)
            session.commit()
            for A in Attendance:
                session.refresh(A)
                return A
            

@app.put("/attendance/{attendance_id}")
def update_attendance_by_id(attendance_id: int, data: attendance, session: Session=Depends(get_session)):
  Attendance=session.get(attendance, attendance_id)
  if not Attendance:
    raise HTTPException(status_code=404, detail="attendance not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(Attendance, key, value)
  session.commit()
  session.refresh(Attendance)
  return Attendance            

                