# Patient Outcomes Tracker

## Problem Statement
In modern healthcare, understanding the real-world effectiveness of treatments and interventions is crucial for improving patient care and optimizing clinical strategies. Traditional methods often rely on periodic assessments that provide a snapshot but fail to capture the dynamic nature of a patient's health journey. This leads to several challenges:

1.  **Delayed Insights:** Health status changes can go unnoticed for extended periods, delaying necessary adjustments to care plans.
2.  **Lack of Granularity:** Aggregate data often masks individual patient trajectories, making it difficult to identify specific factors influencing outcomes.
3.  **Inefficient Resource Allocation:** Without clear, real-time trend data, healthcare providers may struggle to prioritize patients who are deteriorating or to identify successful interventions that can be scaled.
4.  **Limited Proactive Care:** Reacting to acute events rather than proactively managing health trends can lead to worse outcomes and higher costs.

The **Patient Outcomes Tracker** addresses these challenges by providing a system to continuously monitor patient health scores and automatically detect trends (improving, stable, or deteriorating). This enables healthcare professionals to intervene more effectively and provide personalized, proactive care.

## Solution Overview
The Patient Outcomes Tracker is a full-stack application designed to track and visualize patient health outcomes over time. It features a robust backend built with FastAPI and PostgreSQL, responsible for data storage, trend analysis, and API exposure. The frontend, developed with React 19 and TypeScript, provides an intuitive interface for viewing patient lists, their current health scores, and their outcome trends.

The core value of this application lies in its **trend detection logic**. Instead of merely displaying raw scores, the system analyzes the delta between recent health readings to categorize a patient's status as "Improving," "Stable," or "Deteriorating." This allows for quick identification of patients who may require immediate attention or whose treatment plans are proving effective.

## Core Features

*   **Patient Management:** Maintain a list of patients with their demographic and condition information.
*   **Outcome Tracking:** Record and store patient health scores over time, each with a timestamp.
*   **Real-time Trend Analysis:** Automatically calculate and display health trends for each patient based on their recent outcome scores.
    *   **Improving:** Health score shows a significant positive delta.
    *   **Stable:** Health score remains relatively consistent.
    *   **Deteriorating:** Health score shows a significant negative delta.
*   **Colour-Coded Badges:** Visual cues on the frontend to quickly identify patient trends.
*   **FastAPI Backend:**
    *   `GET /patients`: Retrieve a list of patients, with optional filtering by condition. Includes calculated trend and current score.
    *   `POST /outcomes`: Submit new outcome readings for a patient.
    *   `GET /patients/{id}/trend`: Get detailed trend history for a specific patient.
*   **PostgreSQL Database:** Persistent storage for patient and outcome data.
*   **Kafka Event Stub:** A mock in-memory Kafka publisher that simulates publishing an `outcome.submitted` event whenever a new outcome is recorded. This demonstrates how the system could integrate with real-time data streaming platforms for further processing or alerting.
*   **Comprehensive Testing:**
    *   **Backend:** Pytest tests for API endpoints and trend logic.
    *   **Frontend:** Vitest and React Testing Library tests for components and application logic.
*   **CI/CD with GitHub Actions:** Automated testing for both frontend and backend on every push and pull request.
*   **Docker Compose:** Easy local setup and deployment of the entire stack (PostgreSQL, FastAPI, Nginx-served React app).

## Technical Stack

*   **Frontend:**
    *   React 19
    *   TypeScript
    *   Vite (build tool)
    *   TanStack React Query (data fetching and caching)
    *   Tailwind CSS (styling)
    *   Vitest & React Testing Library (testing)
*   **Backend:**
    *   Python 3.11
    *   FastAPI (web framework)
    *   SQLAlchemy (ORM)
    *   PostgreSQL (database)
    *   `kafka-python-ng` (for Kafka stub, though in-memory for this demo)
    *   Pytest (testing)
*   **Infrastructure:**
    *   Docker & Docker Compose
    *   GitHub Actions (CI)

## Setup and Local Development

To get the Patient Outcomes Tracker up and running on your local machine, follow these steps:

### Prerequisites

*   Docker and Docker Compose installed.
*   Git installed.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/patient-outcomes-tracker.git
cd patient-outcomes-tracker
```

### 2. Build and Run with Docker Compose

Navigate to the root of the project and run Docker Compose. This will build the Docker images for both frontend and backend, set up the PostgreSQL database, and start all services.

```bash
docker-compose up --build
```

Wait for all services to start. You can check the logs to ensure everything is running correctly.

### 3. Access the Application

*   **Frontend:** Open your web browser and navigate to `http://localhost:80`
*   **Backend API (Swagger UI):** Access the API documentation at `http://localhost:8000/docs`

### 4. Seed Initial Data (Optional)

To populate the database with some sample patients and outcomes, you can make a `POST` request to the `/seed` endpoint:

```bash
curl -X POST http://localhost:8000/seed
```

Refresh the frontend to see the seeded data.

### 5. Running Tests

#### Backend Tests

To run backend tests (requires Python and pip installed locally, or you can run inside the backend container):

```bash
cd backend
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt pytest httpx
pytest
```

#### Frontend Tests

To run frontend tests (requires Node.js and pnpm installed locally, or you can run inside the frontend container):

```bash
cd frontend
pnpm install
pnpm test
```

## Project Structure

```
patient-outcomes-tracker/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow
├── backend/
│   ├── Dockerfile             # Dockerfile for FastAPI backend
│   ├── requirements.txt       # Python dependencies
│   ├── main.py                # FastAPI application entry point
│   ├── models.py              # SQLAlchemy models for database
│   ├── database.py            # Database connection and session setup
│   ├── trends.py              # Logic for patient trend calculation
│   ├── kafka_stub.py          # Mock Kafka event publisher
│   └── test_main.py           # Pytest tests for backend
├── frontend/
│   ├── Dockerfile             # Dockerfile for React frontend
│   ├── package.json           # Frontend dependencies
│   ├── pnpm-lock.yaml         # pnpm lock file
│   ├── public/
│   ├── src/
│   │   ├── App.tsx            # Main React application component
│   │   ├── index.css          # Tailwind CSS directives
│   │   ├── main.tsx           # React entry point
│   │   ├── types.ts           # TypeScript interfaces
│   │   ├── components/
│   │   │   └── TrendBadge.tsx # React component for trend display
│   │   └── test/
│   │       └── setup.ts       # Vitest setup file
│   ├── vite.config.ts         # Vite configuration with Vitest setup
│   └── App.test.tsx           # Vitest tests for frontend
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # Project README
```

## Future Enhancements

*   **Advanced Trend Analysis:** Implement more sophisticated algorithms for trend detection (e.g., statistical regression, machine learning models) that consider more data points and historical context.
*   **User Authentication:** Add secure user login and role-based access control.
*   **Real Kafka Integration:** Replace the mock Kafka stub with a real Kafka producer and consumer setup for asynchronous event processing.
*   **Notifications and Alerts:** Implement a system to send automated notifications to healthcare providers when a patient's trend deteriorates.
*   **Interactive Charts:** Integrate charting libraries (e.g., Chart.js, Recharts) to visualize patient score history and trends on the frontend.
*   **Admin Dashboard:** A dedicated interface for managing patients, conditions, and system settings.
*   **Deployment Automation:** Scripts or configurations for deploying the application to cloud platforms (e.g., AWS, GCP, Azure).
