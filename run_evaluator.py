import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

django.setup()

from lesson.services.evaluator import (
    evaluate_lesson,
    evaluation_passed,
    get_failed_checks,
    get_regeneration_feedback,
)


# BAD_LESSON = """
# # Introduction to RAG

# RAG stands for Repeated Artificial Generation.

# RAG works by retraining the AI model every time a user
# asks a question. This means the model permanently learns
# the information from the user's question.

# Embeddings are secret instructions inside the AI that
# humans do not need to understand.

# A vector database is simply another name for a neural network
# that trains the AI.

# RAG is mainly used to generate images.

# For example, when you ask RAG a question, it changes the
# AI's training data and makes the model permanently remember
# the answer.
# """


# BAD_LESSON_2 = """
# # Introduction to RAG

# RAG stands for Retrieval-Augmented Generation.

# RAG is a method that helps an AI system answer questions
# using information from documents.

# First, let's understand the important words.

# An AI system is a computer program that can perform tasks
# such as understanding questions and generating answers.

# A document is a piece of written information, such as a
# company policy, a textbook page, or a news article.

# A language model is an AI program that can understand text
# and generate new text.

# Now let's see how RAG works.

# Suppose an employee asks:

# "How many days of leave can I take?"

# The company has a document containing its leave policy.

# 1. The RAG system receives the question.
# 2. It searches the company's documents and finds the part
#    related to leave.
# 3. It gives that useful information to the language model.
# 4. The language model uses the information to write a clear
#    answer.

# The process of finding useful information from documents is
# called retrieval.

# The process of creating a new answer from that information
# is called generation.

# Think of RAG like a student using a textbook before answering
# an exam question. The student first finds the useful page and
# then uses it to write the answer.

# RAG is useful when an AI system needs information from
# external documents, especially when that information can
# change over time.

# In simple terms:

# Question
# → find useful information
# → give it to the language model
# → generate an answer.

# Quick recap:

# - RAG means Retrieval-Augmented Generation.
# - Retrieval means finding useful information.
# - Generation means creating an answer.
# - RAG helps an AI use information from documents when
#   answering a question.
# """


GOOD_LESSON = """
# Introduction to RAG

RAG stands for Retrieval-Augmented Generation.

RAG is a method that helps an AI system answer questions
using information from documents.

First, let's understand the important words.

An AI system is a computer program that can perform tasks
such as understanding questions and generating answers.

A document is a piece of written information, such as a
company policy, a textbook page, or a news article.

A language model is an AI program that can understand text
and generate new text.

Now let's see how RAG works.

Suppose an employee asks:

"How many days of leave can I take?"

The company has a document containing its leave policy.

1. The RAG system receives the question.
2. It searches the company's documents and finds the part
   related to leave.
3. It gives that useful information to the language model.
4. The language model uses the information to write a clear
   answer.

The process of finding useful information from documents is
called retrieval.

The process of creating a new answer from that information
is called generation.

Think of RAG like a student using a textbook before answering
an exam question. The student first finds the useful page and
then uses it to write the answer.

RAG is useful when an AI system needs information from
external documents, especially when that information can
change over time.

In simple terms:

Question
→ find useful information
→ give it to the language model
→ generate an answer.

Quick recap:

- RAG means Retrieval-Augmented Generation.
- Retrieval means finding useful information.
- Generation means creating an answer.
- RAG helps an AI use information from documents when
  answering a question.
"""

print("\n" + "=" * 80)
print("TESTING EVALUATOR")
print("=" * 80)

print("\nLesson being evaluated:")
print(GOOD_LESSON)


evaluation = evaluate_lesson(
    topic="Introduction to RAG",
    lesson=GOOD_LESSON,
)


print("\n" + "=" * 80)
print("EVALUATION RESULT")
print("=" * 80)


checks = {
    "accuracy": evaluation.accuracy,
    "beginner_friendly": evaluation.beginner_friendly,
    "examples": evaluation.examples,
    "jargon": evaluation.jargon,
    "coverage": evaluation.coverage,
    "flow": evaluation.flow,
}


for name, result in checks.items():

    status = "PASS" if result.passed else "FAIL"

    print(f"\n{name.upper()}: {status}")
    print(f"Reason: {result.reason}")
    print(f"Feedback: {result.feedback}")


print("\n" + "=" * 80)
print("OVERALL RESULT")
print("=" * 80)

passed = evaluation_passed(evaluation)

print(
    "PASSED"
    if passed
    else "REJECTED"
)


print("\nFailed checks:")

failed_checks = get_failed_checks(
    evaluation
)

if failed_checks:
    for check in failed_checks:
        print(f"- {check}")
else:
    print("- None")


print("\nRegeneration feedback:")

feedback = get_regeneration_feedback(
    evaluation
)

if feedback:
    for item in feedback:
        print(f"- {item}")
else:
    print("- None")