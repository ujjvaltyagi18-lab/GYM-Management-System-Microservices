from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import salary
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user

app = FastAPI(
    title="Salary Service",
    description="Salary management service",
    version="1.0.0",
    root_path="/api/salary/"
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
    return {"status": "healthy", "service": "salary-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Salary Service", "version": "1.0.0"}


@app.post("/salary/")
def create_salary(Salary: salary, session: Session=Depends(get_session)):
    session.add(Salary)
    session.commit()
    session.refresh(Salary)
    return Salary


@app.get("/salary/")
def get_all_salary(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
):
    return session.exec(select(salary)).all()


@app.get("/salary/{salary_id}")
def get_salary_by_id(salary_id: int, session: Session=Depends(get_session)):
    Salary=session.get(salary, salary_id)
    return Salary


@app.delete("/salary/", status_code=204)
def delete_salary(session: Session=Depends(get_session)):
    Salary=session.exec(select(salary)).all()
    for S in Salary:
        session.delete(S)
        session.commit()
    return {"detail": "all salaries deleted"}

 
@app.delete("/salary/{salary_id}", status_code=204)
def delete_salary_by_id(salary_id: int, session: Session=Depends(get_session)):
    Salary=session.get(salary, salary_id)
    if not Salary:
        raise  HTTPException(status_code=404, detail="salary not found")
    session.delete(Salary)
    session.commit()
    return{"detail": f"salary {salary_id}deleted"} 
     

@app.put("/salary/")
def update_salary(data: salary, session: Session=Depends(get_session)):
    Salary=session.exec(select(salary)).all()
    if not Salary:
        raise HTTPException(status_code=404, detail="salary not found")
    update_data=data.dict(exclude_unset=True)
    for S in Salary:
        for key, value in update_data.items():
            setattr(S, key, value)
            session.commit()
            for S in Salary:
                session.refresh(S)
                return S
            

@app.put("/salary/{salary_id}")
def update_salary_by_id(salary_id: int, data: salary, session: Session=Depends(get_session)):
  Salary=session.get(salary, salary_id)
  if not Salary:
    raise HTTPException(status_code=404, detail="salary not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(Salary, key, value)
  session.commit()
  session.refresh(Salary)
  return Salary 