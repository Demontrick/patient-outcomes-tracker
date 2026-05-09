import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base
import models

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

def test_create_patient_and_get_list():
    # Seed a patient manually for test
    db = TestingSessionLocal()
    p = models.Patient(name="Test Patient", age=50, condition="Test Condition")
    db.add(p)
    db.commit()
    
    response = client.get("/patients")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Patient"

def test_trend_logic_improving():
    db = TestingSessionLocal()
    p = models.Patient(name="Trend Patient", age=50, condition="Test")
    db.add(p)
    db.commit()
    
    # Add outcomes: 70 then 80 (delta +10 > 5)
    client.post("/outcomes", json={"patient_id": p.id, "score": 70})
    client.post("/outcomes", json={"patient_id": p.id, "score": 80})
    
    response = client.get("/patients")
    assert response.json()[0]["trend"] == "Improving"

def test_trend_logic_deteriorating():
    db = TestingSessionLocal()
    p = models.Patient(name="Trend Patient", age=50, condition="Test")
    db.add(p)
    db.commit()
    
    # Add outcomes: 80 then 70 (delta -10 < -5)
    client.post("/outcomes", json={"patient_id": p.id, "score": 80})
    client.post("/outcomes", json={"patient_id": p.id, "score": 70})
    
    response = client.get("/patients")
    assert response.json()[0]["trend"] == "Deteriorating"

def test_get_patient_trend_endpoint():
    db = TestingSessionLocal()
    p = models.Patient(name="Trend Patient", age=50, condition="Test")
    db.add(p)
    db.commit()
    
    client.post("/outcomes", json={"patient_id": p.id, "score": 75})
    
    response = client.get(f"/patients/{p.id}/trend")
    assert response.status_code == 200
    assert "trend" in response.json()
    assert response.json()["current_score"] == 75
