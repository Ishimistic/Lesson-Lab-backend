# Lesson Lab - Backend

An agentic educational content system built with Django, LangChain, Python, and an LLM.

The system generates a beginner-friendly lesson, evaluates it against a strict pass/fail rubric, regenerates rejected lessons using evaluator feedback, and stores recurring failure patterns as persistent memory.

## Objective

Its objective is to take a user-provided topic, generate a standalone beginner-friendly lesson using an LLM, evaluate the generated lesson against a strict quality rubric, and automatically regenerate the lesson when evaluation fails.

The backend also maintains persistent records of generation attempts, evaluator feedback, rejection history, and recurring failure patterns so that the system can learn from previous failures.

The backend exposes this functionality through a Django REST API, while keeping lesson generation, evaluation, retry logic, memory, and persistence separate from the frontend.

## Workflow
```bash
User
  │
  │ topic
  ▼
Django API
  │
  ▼
Lesson Generator
  │
  ▼
Lesson Evaluator
  │
  ▼
Is the lesson good enough?
  │
  ├────────────── YES ──────────────► Final Output
  │
  NO
  │
  ▼
Log Rejection
  │
  ▼
Update Persistent Memory
  │
  ▼
Regenerate Using Evaluator Feedback
  │
  ▼
Evaluate Again
  │
  └──────────────► PASS / Retry
```

Maximum retries are bounded to two.

## Quality Rubric

The evaluator checks:

1. Accuracy
The lesson must contain factually correct explanations and examples without misleading claims.

2. Beginner friendliness
The lesson must be understandable to someone starting from zero and should use simple, clear language.

3. Examples
The lesson must contain at least one concrete example that helps explain the topic.

4. Jargon
Important technical terms must be explained before the learner is expected to understand them.

5. Coverage
The lesson must explain:
- What the topic is
- Why it matters
- How it works

6. Teaching flow
The lesson should move logically from simple concepts to more detailed concepts and end with a useful recap.


Every criterion is PASS or FAIL.

Partial credit is not allowed.

## Architecture

Django is responsible for:

- API endpoints
- reuest handling
- request validation
- database persistence


LangChain is responsible for:

- Prompt construction
- LLM interaction
- lesson generation
- structured evaluation output

Groq
Groq provides the model inference used by the generator and evaluator.

The current model configuration is:
```bash
openai/gpt-oss-20b
```

Python controls:

- Workflow orchestration
- Retry logic
- Termination conditions
- Rubric aggregation
- Memory updates
- Rejection logging
- Output generation


## Project Structure 
```bash
rag_lesson_generator/
│
├── manage.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── lesson/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   │
│   ├── services/
│   │   ├── generator.py
│   │   ├── evaluator.py
│   │   ├── memory.py
│   │   ├── workflow.py
│   │   ├── logger.py
│   │   └── llm.py
│   │
│   ├── prompts/
│   │   ├── generator.py
│   │   └── evaluator.py
│   │
│   └── schemas/
│       └── evaluation.py
│
├── outputs/
│   ├── final_lesson.md
│   └── rejection_log.json
│
├── run_generator.py
├── run_evaluator.py
├── run_demo.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```


## Core Components
### generator.py

Generates the lesson using the topic, persistent memory, and evaluator feedback.

On regeneration, the previous lesson and failed evaluation feedback are passed back to the generator so that it can improve the content.

### evaluator.py

Evaluates the lesson against the six hard rubric criteria and returns structured results using a Pydantic schema.

### workflow.py

Orchestrates the complete generate → evaluate → regenerate loop.

### memory.py

Stores recurring evaluator failures and retrieves previous lessons learned for future generations.

### logger.py

Persists every evaluation attempt, including:
- Attempt number
- Pass/fail status
- Failed checks
- Evaluator feedback
- Changes applied during regeneration

### llm.py
Centralizes the Groq model configuration so the rest of the application does not depend directly on provider-specific configuration.


## Persistent Memory

The system stores recurring evaluator failures in the database.

For example:

- unexplained technical jargon
- weak examples
- missing topic coverage

These lessons are passed into future generations. 

This allows the system to learn from repeated failures across different executions instead of treating every run independently.



## Data Models

### LessonRun

Stores one complete generation workflow.

### EvaluationLog

Stores each evaluation attempt.

### Memory

Stores recurring lessons learned from previous failures.


## API

### Generate a lesson

POST:

`/api/lessons/generate/`

Request:

```json
{
    "topic": "Introduction to RAG"
}
```

Example Response
```json
{
    "status": "passed",
    "topic": "Introduction to RAG",
    "attempts": 2,
    "lesson": "...",
    "rejection_log": [
        {
            "attempt": 1,
            "status": "REJECTED",
            "failed_checks": [
                "accuracy",
                "jargon"
            ],
            "feedback": [
                "Correct the inaccurate explanation of RAG.",
                "Explain technical terms before using them."
            ],
            "changes_made": [
                "Applied evaluator feedback to correct the factual explanation.",
                "Added a beginner-friendly explanation of technical terminology."
            ]
        },
        {
            "attempt": 2,
            "status": "PASSED",
            "failed_checks": [],
            "feedback": [],
            "changes_made": []
        }
    ]
}
```


## Setup
1. Create a virtual environment

Windows:
```bash
python -m venv venv
```

Activate it:
```bash
venv\Scripts\Activate.ps1
```

2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Configure environment variables

Create .env from .env.example.

Example:
```bash
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

GROQ_API_KEY=your-groq-api-key

LLM_MODEL=openai/gpt-oss-20b

MAX_LESSON_RETRIES=2
```

4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Start the server
```bash
python manage.py runserver
```

The API will be available at:
```bash
http://127.0.0.1:8000/
```
Running the Application

The main application is the Django API.

Send:
```bash
POST /api/lessons/generate/
```
with:
```bash
{
    "topic": "Introduction to RAG"
}
```

The complete generation, evaluation, regeneration, memory, and logging workflow runs automatically inside the application.


## Development and Demonstration Scripts

The repository also contains small scripts for testing individual parts of the system.

#### run_generator.py

Makes a real LLM call and demonstrates that the generator can produce a lesson.
```bash
python run_generator.py
```
#### run_evaluator.py

Sends a test lesson to the real evaluator and demonstrates the pass/fail rubric and regeneration feedback.

```bash
python run_evaluator.py
```

#### run_demo.py

Runs the complete end-to-end workflow with a deliberately injected factual error.

This is intended to demonstrate:

```bash
Generate
→ Deliberate Error
→ Evaluate
→ Reject
→ Store Feedback
→ Regenerate
→ Evaluate
→ Pass
```

Run:
```bash
python run_demo.py
```

The deliberate error is used only for demonstration and is not part of the normal API workflow.

## Output Files
### outputs/final_lesson.md

Contains the final lesson produced by the workflow.

### outputs/rejection_log.json

Contains the evaluation history for the run, including rejected attempts, evaluator feedback, and regeneration changes.