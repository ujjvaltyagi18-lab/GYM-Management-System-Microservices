from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import feedback
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user


app = FastAPI(
    title="Feedback Service",
    description="Feedback management service",
    version="1.0.0",
    root_path="/api/feedback/"
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
    return {"status": "healthy", "service": "feedback-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Feedback Service", "version": "1.0.0"}


@app.post("/feedback/")
def create_feedback(Feedback: feedback, session: Session=Depends(get_session)):
    session.add(Feedback)
    session.commit()
    session.refresh(Feedback)
    return Feedback


@app.get("/feedback/")
def get_all_feedback(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return session.exec(select(feedback)).all()


@app.get("/feedback/{feedback_id}")
def get_feedback_by_id(feedback_id: int, session: Session=Depends(get_session)):
    Feedback=session.get(feedback, feedback_id)
    return Feedback


@app.delete("/feedback/", status_code=204)
def delete_feedback(session: Session=Depends(get_session)):
    Feedback=session.exec(select(feedback)).all()
    for F in Feedback:
        session.delete(F)
        session.commit()
    return {"detail": "all feedback deleted"}


@app.delete("/feedback/{feedback_id}", status_code=204)
def delete_feedback_by_id(feedback_id: int, session: Session=Depends(get_session)):
    Feedback=session.get(feedback, feedback_id)
    if not Feedback:
        raise  HTTPException(status_code=404, detail="feedback not found")
    session.delete(Feedback)
    session.commit()
    return{"detail": f"feedback {feedback_id}deleted"} 
     

@app.put("/feedback/")
def update_feedback(data: feedback, session: Session=Depends(get_session)):
    Feedback=session.exec(select(feedback)).all()
    if not Feedback:
        raise HTTPException(status_code=404, detail="feedback not found")
    update_data=data.dict(exclude_unset=True)
    for F in Feedback:
        for key, value in update_data.items():
            setattr(F, key, value)
            session.commit()
            for F in Feedback:
                session.refresh(F)
                return F
            

@app.put("/feedback/{feedback_id}")
def update_feedback_by_id(feedback_id: int, data: feedback, session: Session=Depends(get_session)):
  Feedback=session.get(feedback, feedback_id)
  if not Feedback:
    raise HTTPException(status_code=404, detail="feedback not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(Feedback, key, value)
  session.commit()
  session.refresh(Feedback)
  return Feedback            

                