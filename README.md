# Self-Evaluating Lesson Content Generator

## Objective

Build an AI-powered system that takes a technical topic and automatically generates a standalone, beginner-friendly lesson, evaluates the lesson against a strict quality rubric, and regenerates it when the lesson fails.

The target learner is a 12th-grade graduate in India with limited English and no prior AI knowledge.

## Core Workflow

```bash
User
  │
  │ topic
  ▼
Next.js frontend
  │
  ▼
POST /api/lessons/generate/
  │
  ▼
Django REST API
  │
  ▼
Lesson generation
  │
  ▼
Evaluation
  │
  ▼
Regeneration if required
  │
  ▼
Final JSON response
  │
  ▼
Next.js frontend
  │
  ▼
Rendered lesson
+ Evaluation
+ Rejection history
```

The workflow allows a maximum of 2 retries (maximum 3 generation attempts).

## Evaluation Rubric

Every generated lesson is evaluated on six dimensions:

1. Accuracy — technically correct, no misleading claims, valid examples.
2. Beginner-friendly — understandable to the target learner.
3. Examples — concrete and technically valid examples are provided.
4. Jargon — technical terms are explained before or when they are used.
5. Coverage — explains what the topic is, why it matters, and how it works.
6. Flow — logical progression from basic ideas to examples and recap.

The evaluator produces structured results with:
```bash
passed
reason
feedback
```
for each rubric category.

## Self-Correction

When an attempt fails:
```bash
Evaluator feedback
       +
Previous lesson
       +
Memory of previous failures
       ↓
Regenerator
```

The system then produces a revised lesson and evaluates it again.

The rejection log records:
```bash
Attempt
Status
Failed checks
Evaluator feedback
Changes made
```


## Persistent Memory

The system stores recurring failure patterns in the database.

For example:
```bash
Failure type:
Incorrect technical simplification

Lesson learned:
Do not replace an established technical definition
with an oversimplified but incorrect explanation.
```
This memory is reused in future generations so the system can improve across runs.


## Technology Stack

#### Backend

- Django
- Django REST Framework
- Python
- LangChain
- Groq
- SQLite

#### Frontend

- Next.js
- TypeScript
- React
- Tailwind CSS
- React Markdown

The frontend provides:

- Topic input
- Generated lesson viewer
- Evaluation results
- Attempt/rejection history
- Changes made during regeneration



## Future Improvements
#### 1. Dynamic evidence retrieval
Retrieve reliable, topic-specific information before generation instead of depending entirely on the model's internal knowledge.

#### 2. Evidence-based evaluation
Evaluate important technical claims against the retrieved evidence rather than asking the LLM only whether the lesson “sounds accurate.”

#### 3. Claim-level fact checking
Extract important claims from the generated lesson and verify each claim individually. This makes it easier to identify exactly what is wrong.

#### 4. Source reliability ranking
Prefer authoritative sources such as official documentation, universities, government organizations, and established technical references over arbitrary web pages.

#### 5. Adaptive regeneration
Instead of simply sending all feedback back to the generator, regenerate specifically around the failed criteria. For example, an accuracy failure should trigger factual correction rather than a complete rewrite.

#### 6. Improved long-term memory
Store recurring failure patterns and use them to improve future generations, while keeping factual knowledge separate from lessons learned about generation quality.

#### 7. Human review option
For high-risk or highly technical topics, allow a human to review the lesson before it is marked as final.

#### 8. Better source management
Store the sources used for a lesson along with the final output so users can see where the factual information came from.

#### 9. Caching retrieved evidence
Cache evidence for recently requested topics to reduce repeated retrieval and improve response time.

#### 10. Multi-source verification
For important technical claims, compare information from multiple independent sources before accepting the claim.

