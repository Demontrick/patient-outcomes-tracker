# Patient Outcomes Tracker

![CI](https://github.com/Demontrick/patient-outcomes-tracker/actions/workflows/ci.yml/badge.svg)

AI-powered clinical outcomes monitoring platform built with FastAPI, React 19, TypeScript, PostgreSQL, and locally hosted LLM streaming via Ollama.

---

## Overview

Modern healthcare systems often rely on delayed or static assessments that fail to capture how patient conditions evolve over time.

The Patient Outcomes Tracker addresses this by combining:

- Real-time patient outcome tracking
- Trend analysis
- AI-generated clinical recommendations
- Streaming UX
- Modern full-stack architecture

The platform allows healthcare teams to:

- Monitor patient health trajectories
- Identify deteriorating patients early
- Visualize outcome trends
- Generate contextual AI-powered recommendations
- Continuously update patient outcome records

---

## Core Features

### Patient Management
- Track patient demographic and clinical information
- View condition-specific patient groups
- Filter patients by condition instantly

### Outcome Tracking
- Submit new health outcome scores
- Persist patient history in PostgreSQL
- Automatically refresh frontend state after mutations

### Trend Analysis

Each patient receives a calculated health trend:

| Trend | Meaning |
|---|---|
| ✅ Improving | Score delta is positive |
| ➡️ Stable | Score delta is minimal |
| ⚠️ Deteriorating | Score delta is negative |

Trend calculations are derived from recent patient outcome deltas.

### AI Clinical Recommendations

Each patient card includes an **AI Insight** action that generates contextual clinical recommendations in real time. Recommendations stream progressively into the UI instead of waiting for the full response.

---

## AI Clinical Insight Engine

One of the core features of this project is the AI-powered clinical recommendation system.

When a user clicks the **"AI Insight"** button on a patient card, the frontend sends a streaming request to the backend, which generates contextual clinical recommendations using a locally hosted LLM through Ollama.

### Model Used

- qwen2.5:0.5b
- Served locally using Ollama
- Streaming responses enabled for real-time UI updates

### Why This Model?

The qwen2.5:0.5b model was selected because it is:

- Lightweight and fast for local development
- Efficient enough to run on consumer hardware
- Capable of producing structured recommendation-style responses
- Suitable for streaming token-by-token outputs with low latency

This allowed the project to demonstrate real-time AI integration without relying on external paid APIs.

### AI Request Flow

1. User clicks **AI Insight**
2. React frontend sends request to /patients/{id}/insight
3. FastAPI backend:
   - Loads patient data
   - Builds a clinical context prompt
   - Sends request to Ollama
4. Ollama streams generated tokens
5. Backend converts tokens into SSE events
6. Frontend progressively renders recommendations in real time

### Streaming Architecture

The backend streams responses using **Server-Sent Events (SSE)**.

The frontend consumes the stream incrementally using:

- ReadableStream
- TextDecoder
- AbortController

This enables:

- Real-time rendering
- Cancellable requests
- Smoother UX
- Non-blocking AI interactions

### Structured Stream Handling

The backend streams events in SSE format:

json
{
  "type": "chunk",
  "content": "..."
}


The frontend transforms these low-level stream events into clean recommendation panels so users never see raw JSON or transport-layer data.

### Example AI Recommendations

The AI layer can generate:

- Monitoring recommendations
- Lifestyle intervention suggestions
- Medication adherence reminders
- Follow-up guidance
- Risk-awareness recommendations

> The AI system is designed as a **clinical support feature** rather than a diagnostic engine.

---

## Product Engineering Decisions

### Real-Time Streaming UX
Instead of waiting for a complete AI response before rendering, the UI streams recommendations progressively for a faster and more responsive user experience.

### React Query for Server State
TanStack React Query was used to cache API responses, simplify async state management, automatically refresh stale data, and reduce unnecessary network requests.

### Type-Safe Frontend
The frontend is fully written in TypeScript to improve API safety, maintainability, component contracts, and developer experience.

### Separation of Concerns
The architecture separates API logic, AI streaming logic, reusable UI components, data-fetching concerns, and presentation logic — keeping the application scalable and maintainable.

### Local-First AI Development
Using Ollama with a locally hosted model enables offline experimentation, lower development costs, faster iteration, and reduced external dependencies.

---

## Technical Stack

### Frontend
| Technology | Purpose |
|---|---|
| React 19 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool |
| TanStack React Query | Server state management |
| Tailwind CSS | Styling |
| Lucide React | Icons |
| Vitest + React Testing Library | Testing |

### Backend
| Technology | Purpose |
|---|---|
| Python 3.11 | Runtime |
| FastAPI | Web framework |
| SQLAlchemy | ORM |
| PostgreSQL | Database |
| Ollama | Local LLM inference |
| Server-Sent Events | AI response streaming |
| Pytest | Testing |

### Infrastructure
| Technology | Purpose |
|---|---|
| Docker + Docker Compose | Containerisation |
| GitHub Actions | CI/CD |

---

## API Endpoints

### Get Patients
http
GET /patients

Optional filter:
http
GET /patients?condition=diabetes

Returns patient information, current score, and calculated trend.

### Create Outcome
http
POST /outcomes

json
{
  "patient_id": 1,
  "score": 85
}


### Generate AI Insight
http
POST /patients/{id}/insight

Returns a streaming SSE response.

---

## Kafka Event Stub

The backend includes a lightweight Kafka-style event stub that simulates publishing `outcome.submitted` events whenever a new patient outcome is recorded.

This demonstrates how the system could later integrate with Kafka, event pipelines, alerting systems, and analytics consumers.

---

## Testing

### Backend
Pytest coverage includes:
- API endpoints
- Trend calculation logic
- Outcome submission
- Validation handling

### Frontend
Vitest + React Testing Library tests include:
- Component rendering
- User interactions
- State updates
- Query behavior

---

## CI/CD

GitHub Actions automatically runs frontend tests, backend tests, linting, and validation checks on every push and pull request.

---

## Local Development

### Prerequisites
- Docker and Docker Compose
- Node.js
- Python 3.11
- Ollama

### Run Ollama
bash
ollama pull qwen2.5:0.5b

Start Ollama locally before running the backend.

### Clone Repository
bash
git clone https://github.com/Demontrick/patient-outcomes-tracker.git
cd patient-outcomes-tracker


### Start Application
bash
docker-compose up --build


### Access Application
- **Frontend:** http://localhost:80
- **Backend API docs:** http://localhost:8000/docs

### Seed Sample Data
bash
curl -X POST http://localhost:8000/seed


### Run Frontend Locally
bash
cd frontend
npm install
npm run dev


### Run Backend Locally
bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload


---

## Project Structure


patient-outcomes-tracker/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── trends.py
│   ├── kafka_stub.py
│   ├── ai.py
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.tsx
│   │   ├── types.ts
│   │   └── main.tsx
│   ├── vite.config.ts
│   └── package.json
│
├── docker-compose.yml
└── README.md


---

## Future Enhancements

- Retrieval-Augmented Generation (RAG)
- Vector database integration
- Historical trend summarization
- Physician review workflows
- Structured AI outputs
- Advanced analytics dashboards
- Real-time notifications
- Multi-patient risk prediction
- Healthcare-specific fine-tuned models

---

## Key Takeaways

This project demonstrates:

- Full-stack TypeScript + Python development
- Real-time streaming architectures
- AI integration with local LLMs
- Product-focused frontend engineering
- Scalable API design
- Async state management
- Modern React patterns
- Responsive UX design
- Production-style architecture decisions
AI integration with local LLMs
product-focused frontend engineering
scalable API design
async state management
modern React patterns
responsive UX design
production-style architecture decisions
