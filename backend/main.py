from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import models, trends, kafka_stub
from database import SessionLocal, engine
from pydantic import BaseModel
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Patient Outcomes Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class OutcomeCreate(BaseModel):
    patient_id: int
    score: float

class OutcomeResponse(BaseModel):
    id: int
    patient_id: int
    score: float
    timestamp: datetime
    model_config = {"from_attributes": True}

class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    condition: str
    trend: Optional[str] = "Stable"
    current_score: Optional[float] = None
    model_config = {"from_attributes": True}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/patients", response_model=List[PatientResponse])
def get_patients(condition: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Patient)
    if condition:
        query = query.filter(models.Patient.condition == condition)
    
    patients = query.all()
    results = []
    for p in patients:
        trend_data = trends.get_patient_trend_data(p.outcomes)
        results.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "condition": p.condition,
            "trend": trend_data["trend"],
            "current_score": trend_data["current_score"]
        })
    return results

@app.post("/outcomes", response_model=OutcomeResponse)
def create_outcome(outcome: OutcomeCreate, db: Session = Depends(get_db)):
    db_outcome = models.Outcome(**outcome.model_dump())
    db.add(db_outcome)
    db.commit()
    db.refresh(db_outcome)
    
    # Publish mock Kafka event
    kafka_stub.publish_outcome_event(outcome.patient_id, outcome.score)
    
    return db_outcome

@app.get("/patients/{patient_id}/trend")
def get_patient_trend(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return trends.get_patient_trend_data(patient.outcomes)

@app.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    # Simple seed for development
    if db.query(models.Patient).count() == 0:
        p1 = models.Patient(name="John Doe", age=45, condition="Hypertension")
        p2 = models.Patient(name="Jane Smith", age=32, condition="Diabetes")
        db.add_all([p1, p2])
        db.commit()
        
        o1 = models.Outcome(patient_id=p1.id, score=70, timestamp=datetime(2024, 1, 1))
        o2 = models.Outcome(patient_id=p1.id, score=75, timestamp=datetime(2024, 2, 1))
        o3 = models.Outcome(patient_id=p2.id, score=90, timestamp=datetime(2024, 1, 1))
        o4 = models.Outcome(patient_id=p2.id, score=80, timestamp=datetime(2024, 2, 1))
        db.add_all([o1, o2, o3, o4])
        db.commit()
        return {"message": "Data seeded"}
    return {"message": "Already seeded"}
