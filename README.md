# Patient Outcomes Tracker

![CI](https://github.com/Demontrick/patient-outcomes-tracker/actions/workflows/ci.yml/badge.svg)
AI-powered clinical outcomes monitoring platform built with FastAPI, React 19, TypeScript, PostgreSQL, and locally hosted LLM streaming via Ollama.

---

## Overview

Modern healthcare systems often rely on delayed or static assessments that fail to capture how patient conditions evolve over time.

The Patient Outcomes Tracker addresses this by combining:

- real-time patient outcome tracking
- trend analysis
- AI-generated clinical recommendations
- streaming UX
- modern full-stack architecture

The platform allows healthcare teams to:

- monitor patient health trajectories
- identify deteriorating patients early
- visualize outcome trends
- generate contextual AI-powered recommendations
- continuously update patient outcome records

---

# Core Features

## Patient Management

- Track patient demographic and clinical information
- View condition-specific patient groups
- Filter patients by condition instantly

---

## Outcome Tracking

- Submit new health outcome scores
- Persist patient history in PostgreSQL
- Automatically refresh frontend state after mutations

---

## Trend Analysis

Each patient receives a calculated health trend:

- Improving
- Stable
- Deteriorating

Trend calculations are derived from recent patient outcome deltas.

---

## AI Clinical Recommendations

Each patient card includes an **AI Insight** action that generates contextual clinical recommendations in real time.

The recommendations stream progressively into the UI instead of waiting for the full response.

---

# AI Clinical Insight Engine

One of the core features of this project is the AI-powered clinical recommendation system.

When a user clicks the **"AI Insight"** button on a patient card, the frontend sends a streaming request to the backend, which generates contextual clinical recommendations using a locally hosted LLM through Ollama.

---

## Model Used

- `qwen2.5:0.5b`
- Served locally using Ollama
- Streaming responses enabled for real-time UI updates

---

## Why This Model?

The `qwen2.5:0.5b` model was selected because it is:

- lightweight and fast for local development
- efficient enough to run on consumer hardware
- capable of producing structured recommendation-style responses
- suitable for streaming token-by-token outputs with low latency

This allowed the project to demonstrate real-time AI integration without relying on external paid APIs.

---

## AI Request Flow

1. User clicks **AI Insight**
2. React frontend sends request to:
   `/patients/{id}/insight`
3. FastAPI backend:
   - loads patient data
   - builds a clinical context prompt
   - sends request to Ollama
4. Ollama streams generated tokens
5. Backend converts tokens into SSE events
6. Frontend progressively renders recommendations in real time

---

## Streaming Architecture

The backend streams responses using **Server-Sent Events (SSE)**.

The frontend consumes the stream incrementally using:

- `ReadableStream`
- `TextDecoder`
- `AbortController`

This enables:

- real-time rendering
- cancellable requests
- smoother UX
- non-blocking AI interactions

---

## Structured Stream Handling

The backend streams events in SSE format:

```json
{
  "type": "chunk",
  "content": "..."
}

The frontend transforms these low-level stream events into clean recommendation panels so users never see raw JSON or transport-layer data.

Example AI Recommendations

The AI layer can generate:

monitoring recommendations
lifestyle intervention suggestions
medication adherence reminders
follow-up guidance
risk-awareness recommendations

The AI system is designed as a clinical support feature rather than a diagnostic engine.

Product Engineering Decisions

This project was intentionally designed with product engineering principles in mind.

Real-Time Streaming UX

Instead of waiting for a complete AI response before rendering, the UI streams recommendations progressively for a faster and more responsive user experience.

React Query for Server State

TanStack React Query was used to:

cache API responses
simplify async state management
automatically refresh stale data
reduce unnecessary network requests
Type-Safe Frontend

The frontend is fully written in TypeScript to improve:

API safety
maintainability
component contracts
developer experience
Separation of Concerns

The architecture separates:

API logic
AI streaming logic
reusable UI components
data-fetching concerns
presentation logic

This keeps the application scalable and maintainable.

Local-First AI Development

Using Ollama with a locally hosted model enables:

offline experimentation
lower development costs
faster iteration
reduced external dependencies
Performance & UX Considerations

Several UX-focused improvements were implemented:

streaming AI responses
instant patient filtering
optimistic data refresh
lightweight rendering
cancelable AI requests
responsive Tailwind layout
clean recommendation formatting

The application prioritizes perceived responsiveness and clarity of information.

Technical Stack
Frontend
React 19
TypeScript
Vite
TanStack React Query
Tailwind CSS
Lucide React
Vitest
React Testing Library
Backend
Python 3.11
FastAPI
SQLAlchemy
PostgreSQL
Ollama
Server-Sent Events (SSE)
Pytest
Infrastructure
Docker
Docker Compose
GitHub Actions CI
API Endpoints
Patients
Get Patients
GET /patients

Optional query parameter:

GET /patients?condition=diabetes

Returns:

patient information
current score
calculated trend
Create Outcome
POST /outcomes

Body:

{
  "patient_id": 1,
  "score": 85
}
Generate AI Insight
POST /patients/{id}/insight

Returns streaming SSE response.

Kafka Event Stub

The backend includes a lightweight Kafka-style event stub that simulates publishing:

outcome.submitted

events whenever a new patient outcome is recorded.

This demonstrates how the system could later integrate with:

Kafka
event pipelines
alerting systems
analytics consumers
Testing
Backend

Pytest coverage includes:

API endpoints
trend calculation logic
outcome submission
validation handling
Frontend

Vitest + React Testing Library tests include:

component rendering
user interactions
state updates
query behavior
CI/CD

GitHub Actions automatically runs:

frontend tests
backend tests
linting
validation checks

on every push and pull request.

Local Development
Prerequisites
Docker
Docker Compose
Node.js
Python 3.11
Ollama
Run Ollama

Install model:

ollama pull qwen2.5:0.5b

Start Ollama locally before running the backend.

Clone Repository
git clone https://github.com/your-username/patient-outcomes-tracker.git

cd patient-outcomes-tracker
Start Application
docker-compose up --build
Access Application

Frontend:

http://localhost:80

Backend:

http://localhost:8000/docs
Seed Sample Data
curl -X POST http://localhost:8000/seed
Run Frontend Locally
cd frontend

npm install

npm run dev
Run Backend Locally
cd backend

python -m venv venv

Linux / macOS:

source venv/bin/activate

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn main:app --reload
Project Structure
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
Future Enhancements

Potential next steps include:

Retrieval-Augmented Generation (RAG)
vector database integration
historical trend summarization
physician review workflows
structured AI outputs
advanced analytics dashboards
real-time notifications
multi-patient risk prediction
healthcare-specific fine-tuned models
Key Takeaways

This project demonstrates:

full-stack TypeScript + Python development
real-time streaming architectures
AI integration with local LLMs
product-focused frontend engineering
scalable API design
async state management
modern React patterns
responsive UX design
production-style architecture decisions