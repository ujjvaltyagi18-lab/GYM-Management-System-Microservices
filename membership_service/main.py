from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import Plan, Membership
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user



app = FastAPI(
    title="Membership Service",
    description="Membership management service",
    version="1.0.0",
    root_path="/api/membership/"
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
    return {"status": "healthy", "service": "membership-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Membership Service", "version": "1.0.0"}


@app.post("/plans/")
def create_plans(plan: Plan, session: Session=Depends(get_session)):
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@app.get("/plans/")
def get_all_plans(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
):
    return session.exec(select(Plan)).all()


@app.get("/plans/{plan_id}")
def get_plans_by_id(plan_id: int, session: Session=Depends(get_session)):
    plan=session.get(Plan, plan_id)
    return plan


@app.delete("/plans/", status_code=204)
def delete_plans(session: Session=Depends(get_session)):
    plan=session.exec(select(Plan)).all()
    for P in plan:
        session.delete(P)
        session.commit()
    return {"detail": "all plans deleted"}


@app.delete("/plans/{plan_id}", status_code=204)
def delete_plans_by_id(plan_id: int, session: Session=Depends(get_session)):
    plan=session.get(Plan, plan_id)
    if not plan:
        raise  HTTPException(status_code=404, detail="Plan not found")
    session.delete(plan)
    session.commit()
    return{"detail": f"Plan {plan_id}deleted"} 
     

@app.put("/plans/")
def update_plans(data: Plan, session: Session=Depends(get_session)):
    plan=session.exec(select(Plan)).all()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    update_data=data.dict(exclude_unset=True)
    for P in plan:
        for key, value in update_data.items():
            setattr(P, key, value)
            session.commit()
            for P in Plan:
                session.refresh(P)
                return P
            

@app.put("/plans/{plan_id}")
def update_plans_by_id(plan_id: int, data: Plan, session: Session=Depends(get_session)):
  plan=session.get(Plan, plan_id)
  if not plan:
    raise HTTPException(status_code=404, detail="Plan not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(plan, key, value)
  session.commit()
  session.refresh(plan)
  return plan         




@app.post("/memberships/")
def create_memberships(membership: Membership, session: Session=Depends(get_session)):
    session.add(membership)
    session.commit()
    session.refresh(membership)
    return membership


@app.get("/memberships/")
def get_all_memberships(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
):
    return session.exec(select(Membership)).all()


@app.get("/memberships/{membership_id}")
def get_memberships_by_id(membership_id: int, session: Session=Depends(get_session)):
    membership=session.get(Membership, membership_id)
    return membership


@app.delete("/memberships/", status_code=204)
def delete_memberships(session: Session=Depends(get_session)):
    membership=session.exec(select(Membership)).all()
    for M in membership:
        session.delete(M)
        session.commit()
    return {"detail": "all memberships deleted"}


@app.delete("/memberships/{membership_id}", status_code=204)
def delete_memberships_by_id(membership_id: int, session: Session=Depends(get_session)):
    membership=session.get(Membership, membership_id)
    if not membership:
        raise  HTTPException(status_code=404, detail="membership not found")
    session.delete(membership)
    session.commit()
    return{"detail": f"membership {membership_id}deleted"} 
     

@app.put("/memberships/")
def update_memberships(data: Membership, session: Session=Depends(get_session)):
    membership=session.exec(select(Membership)).all()
    if not membership:
        raise HTTPException(status_code=404, detail="membership not found")
    update_data=data.dict(exclude_unset=True)
    for M in membership:
        for key, value in update_data.items():
            setattr(M, key, value)
            session.commit()
            for M in membership:
                session.refresh(M)
                return M
            

@app.put("/memberships/{membership_id}")
def update_memberships_by_id(membership_id: int, data: Membership, session: Session=Depends(get_session)):
    membership=session.get(Membership, membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="membership not found")
    for key, value in data.dict(exclude_unset=True):
        setattr(membership, key, value)
    session.commit()
    session.refresh(membership)
    return membership

                