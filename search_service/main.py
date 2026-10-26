from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from model import search
from database import get_session
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from common.security import get_current_user

app = FastAPI(
    title="Search Service",
    description="Search management service",
    version="1.0.0",
    root_path="/api/search/"
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
    return {"status": "healthy", "service": "search-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Search Service", "version": "1.0.0"}


@app.post("/search/")
def create_search(Search: search, session: Session=Depends(get_session)):
    session.add(Search)
    session.commit()
    session.refresh(Search)
    return Search


@app.get("/search/")
def get_all_search(
    current_user=Depends(get_current_user),
    session:Session=Depends(get_session)
):
    return session.exec(select(search)).all()


@app.get("/search/{search_id}")
def get_search_by_id(search_id: int, session: Session=Depends(get_session)):
    Search=session.get(search, search_id)
    return Search


@app.delete("/search/", status_code=204)
def delete_search(session: Session=Depends(get_session)):
    Search=session.exec(select(search)).all()
    for S in Search:
        session.delete(S)
        session.commit()
    return {"detail": "all searches deleted"}

 
@app.delete("/search/{search_id}", status_code=204)
def delete_search_by_id(search_id: int, session: Session=Depends(get_session)):
    Search=session.get(search, search_id)
    if not Search:
        raise  HTTPException(status_code=404, detail="search not found")
    session.delete(Search)
    session.commit()
    return{"detail": f"search {search_id}deleted"} 
     

@app.put("/search/")
def update_search(data: search, session: Session=Depends(get_session)):
    Search=session.exec(select(search)).all()
    if not Search:
        raise HTTPException(status_code=404, detail="search not found")
    update_data=data.dict(exclude_unset=True)
    for S in Search:
        for key, value in update_data.items():
            setattr(S, key, value)
            session.commit()
            for S in Search:
                session.refresh(S)
                return S
            

@app.put("/search/{search_id}")
def update_search_by_id(search_id: int, data: search, session: Session=Depends(get_session)):
  Search=session.get(search, search_id)
  if not Search:
    raise HTTPException(status_code=404, detail="search not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(Search, key, value)
  session.commit()
  session.refresh(Search)
  return Search 