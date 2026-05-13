from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import models, trends, kafka_stub
from database import SessionLocal, engine
from pydantic import BaseModel
from datetime import datetime

import httpx
import json
from fastapi.responses import StreamingResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Patient Outcomes Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Pydantic schemas
# -------------------------

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


# -------------------------
# DB dependency
# -------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Existing endpoints (UNCHANGED)
# -------------------------

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


# -------------------------
# AI INSIGHT (FINAL SAFE VERSION)
# -------------------------

@app.post("/patients/{patient_id}/insight")
async def get_insight(patient_id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    outcomes = (
        db.query(models.Outcome)
        .filter(models.Outcome.patient_id == patient_id)
        .order_by(models.Outcome.timestamp.desc())
        .limit(5)
        .all()
    )

    scores = [o.score for o in outcomes]

    prompt = f"""
Patient: {patient.name}
Condition: {patient.condition}
Recent scores: {scores}

Give 3 short clinical recommendations.
Keep them structured, practical, and concise.
"""

    async def stream():

        # START event
        yield json.dumps({"type": "start"}) + "\n"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream(
                    "POST",
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen2.5:0.5b",
                        "prompt": prompt,
                        "stream": True
                    }
                ) as r:

                    buffer = ""

                    async for line in r.aiter_lines():
                        if not line:
                            continue

                        try:
                            data = json.loads(line)
                            token = data.get("response", "")

                            if token:
                                buffer += token

                                # flush clean chunks
                                if len(buffer) > 80 or token in [".", "\n"]:
                                    yield json.dumps({
                                        "type": "chunk",
                                        "content": buffer.strip()
                                    }) + "\n"
                                    buffer = ""

                        except:
                            continue

                    # flush remaining
                    if buffer:
                        yield json.dumps({
                            "type": "chunk",
                            "content": buffer.strip()
                        }) + "\n"

        except Exception as e:
            # SAFE fallback (important for demos/interviews)
            yield json.dumps({
                "type": "error",
                "message": "AI service unavailable",
                "detail": str(e)
            }) + "\n"

        # END event
        yield json.dumps({"type": "end"}) + "\n"

    return StreamingResponse(stream(), media_type="text/plain")