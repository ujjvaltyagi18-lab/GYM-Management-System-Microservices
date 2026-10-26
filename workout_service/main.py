from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import workout
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user

app = FastAPI(
    title="Workout Service",
    description="Workout management service",
    version="1.0.0",
    root_path="/api/workout/"
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
    return {"status": "healthy", "service": "workout-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Workout Service", "version": "1.0.0"}


@app.post("/workouts/")
def create_workout(Workout: workout, session: Session=Depends(get_session)):
    session.add(Workout)
    session.commit()
    session.refresh(Workout)
    return Workout


@app.get("/workouts/")
def get_all_workouts(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
):
    return session.exec(select(workout)).all()


@app.get("/workouts/{workout_id}")
def get_workout_by_id(workout_id: int, session: Session=Depends(get_session)):
    Workout=session.get(workout, workout_id)
    return Workout


@app.delete("/workouts/", status_code=204)
def delete_workouts(session: Session=Depends(get_session)):
    Workouts=session.exec(select(workout)).all()
    for W in Workouts:
        session.delete(W)
        session.commit()
    return {"detail": "all workouts deleted"}

 
@app.delete("/workouts/{workout_id}", status_code=204)
def delete_workout_by_id(workout_id: int, session: Session=Depends(get_session)):
    Workout=session.get(workout, workout_id)
    if not Workout:
        raise  HTTPException(status_code=404, detail="workout not found")
    session.delete(Workout)
    session.commit()
    return{"detail": f"workout {workout_id}deleted"} 
     

@app.put("/workouts/")
def update_workout(data: workout, session: Session=Depends(get_session)):
    Workouts=session.exec(select(workout)).all()
    if not Workouts:
        raise HTTPException(status_code=404, detail="workout not found")
    update_data=data.dict(exclude_unset=True)
    for W in Workouts:
        for key, value in update_data.items():
            setattr(W, key, value)
            session.commit()
            for W in Workouts:
                session.refresh(W)
                return W

            

@app.put("/workouts/{workout_id}")
def update_workout_by_id(workout_id: int, data: workout, session: Session=Depends(get_session)):
    Workout=session.get(workout, workout_id)
    if not Workout:
        raise HTTPException(status_code=404, detail="workout not found")
    for key, value in data.dict(exclude_unset=True):
        setattr(Workout, key, value)
    session.commit()
    session.refresh(Workout)
    return Workout 