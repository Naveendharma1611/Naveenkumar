"""Seed the Agentic AI category and its 20-question fundamentals quiz.

Usage: python seed_quiz_agentic_ai.py (run from backend/, same venv as manage.py)
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction

from apps.learning.models import StudyCategory
from apps.quizzes.models import Quiz, QuizQuestion

QUESTIONS = [
    {
        "prompt": "What is a common high-level loop for an AI agent?",
        "options": [
            "Receive context, choose an action, execute or request a tool, observe the result, and decide whether to continue",
            "Generate text once and assume the task is complete",
            "Run every available tool before reading the user's goal",
            "Repeat forever until the model changes its own code",
        ],
        "correct_option": 0,
        "explanation": "An agent commonly alternates between reasoning or decision steps, tool actions, and observations until a stop condition is met.",
    },
    {
        "prompt": "What typically happens when a model proposes a tool call?",
        "options": [
            "Application code validates the proposed call and executes an allowed tool",
            "The model automatically receives unrestricted operating-system access",
            "The call is guaranteed to succeed without application code",
            "The tool runs before its arguments are produced",
        ],
        "correct_option": 0,
        "explanation": "The model proposes structured arguments; trusted application code validates permissions and inputs before execution.",
    },
    {
        "prompt": "Why should tool schemas be narrow and explicit?",
        "options": [
            "They make allowed operations and expected arguments easier to validate",
            "They guarantee the model always chooses correctly",
            "They remove the need for authorization",
            "They automatically make a tool idempotent",
        ],
        "correct_option": 0,
        "explanation": "Narrow, typed schemas reduce ambiguity and support input validation, but do not replace authorization or other safeguards.",
    },
    {
        "prompt": "Where should permission checks for a state-changing tool be enforced?",
        "options": [
            "In trusted backend code for each operation",
            "Only in the model's prompt instructions",
            "Only by hiding the tool button in the UI",
            "Only after an action has completed",
        ],
        "correct_option": 0,
        "explanation": "Enforce authorization in trusted backend code; prompts and UI controls are not security boundaries.",
    },
    {
        "prompt": "What is least privilege for an agent tool?",
        "options": [
            "Grant only the minimum access and actions needed for the task",
            "Give the agent administrator access so it cannot fail",
            "Reuse one credential across all tools and users",
            "Allow the tool to ignore user permissions",
        ],
        "correct_option": 0,
        "explanation": "Least privilege limits the potential impact of a model or tool error by granting only necessary capabilities.",
    },
    {
        "prompt": "When is an approval gate especially appropriate?",
        "options": [
            "Before consequential, external, financial, or hard-to-reverse actions",
            "Before every internal string concatenation",
            "Only after a destructive action is complete",
            "As a replacement for authentication",
        ],
        "correct_option": 0,
        "explanation": "Require human confirmation when actions have significant impact or are difficult to undo.",
    },
    {
        "prompt": "What is a key distinction between working state and durable memory?",
        "options": [
            "Working state supports the current task; durable memory persists across runs and needs explicit governance",
            "Working state is always public; durable memory is always private",
            "Durable memory is deleted after every tool call",
            "There is no difference in lifetime or privacy implications",
        ],
        "correct_option": 0,
        "explanation": "Persistent memory can affect future interactions and should have clear consent, access, retention, and deletion rules.",
    },
    {
        "prompt": "What is the role of an observation after a tool executes?",
        "options": [
            "Provide the tool result or error as input to the agent's next decision",
            "Prove that the result is safe and correct without validation",
            "Replace the original task goal permanently",
            "Automatically authorize the next tool call",
        ],
        "correct_option": 0,
        "explanation": "The agent uses tool output as new context, but the application may still need to validate and treat that output as untrusted.",
    },
    {
        "prompt": "Why should an agent loop have a maximum step count or run deadline?",
        "options": [
            "To bound runaway behavior, latency, and cost",
            "To guarantee every goal is completed",
            "To prevent the model from using any tools",
            "To make audit logs unnecessary",
        ],
        "correct_option": 0,
        "explanation": "Step, time, and cost budgets limit unproductive loops and make service behavior more predictable.",
    },
    {
        "prompt": "Why can retrying a tool call be dangerous?",
        "options": [
            "A repeated call may duplicate a side effect unless the operation is idempotent or protected",
            "Retries always delete the original result",
            "Retries disable authentication",
            "A second call always returns the same output",
        ],
        "correct_option": 0,
        "explanation": "Network failures can make completion uncertain; use bounded retries and idempotency keys or safeguards for side-effecting operations.",
    },
    {
        "prompt": "What is prompt injection in an agent system?",
        "options": [
            "Untrusted user or retrieved content attempts to override instructions or misuse tools",
            "A method for compressing agent memory",
            "A guaranteed way to improve task success",
            "A tool schema validation error only",
        ],
        "correct_option": 0,
        "explanation": "Prompt injection uses untrusted content to influence behavior; enforce boundaries and permissions outside the prompt.",
    },
    {
        "prompt": "How should an agent application treat text returned by a search tool?",
        "options": [
            "As untrusted data that may contain misleading instructions or malicious content",
            "As system instructions with higher priority than application policy",
            "As automatically verified truth",
            "As safe executable code by default",
        ],
        "correct_option": 0,
        "explanation": "Retrieved content is data, not trusted policy; validate, constrain, and separate it from instructions.",
    },
    {
        "prompt": "What does an agent evaluation set help measure?",
        "options": [
            "Task success and failure behavior on representative scenarios",
            "Whether the model's internal thoughts are always correct",
            "The exact latency of every future production request",
            "Authorization without testing backend rules",
        ],
        "correct_option": 0,
        "explanation": "Representative evaluations measure task outcomes and failure modes, but do not guarantee future production behavior.",
    },
    {
        "prompt": "Why record an agent trace with tool calls and observations?",
        "options": [
            "To diagnose where a run diverged, failed, or exceeded policy",
            "To store every secret in plaintext for debugging",
            "To guarantee a future run is deterministic",
            "To replace user-facing error handling",
        ],
        "correct_option": 0,
        "explanation": "Traces help reconstruct execution and investigate failures; redact sensitive information and apply retention controls.",
    },
    {
        "prompt": "What does a sandbox help limit?",
        "options": [
            "The resources and effects available to code or tools during execution",
            "The number of tokens in every model vocabulary",
            "The accuracy of every model output",
            "The user's network connection speed",
        ],
        "correct_option": 0,
        "explanation": "A sandbox can isolate execution and constrain file, network, CPU, memory, and other capabilities.",
    },
    {
        "prompt": "What is a useful response when an agent cannot complete a task safely?",
        "options": [
            "Stop, report the limitation, and request clarification or human review when appropriate",
            "Continue calling tools until one succeeds",
            "Hide the failure and claim success",
            "Expand permissions automatically",
        ],
        "correct_option": 0,
        "explanation": "A safe fallback can stop execution, surface uncertainty, and request clarification or an authorized review.",
    },
    {
        "prompt": "What should a multi-agent design justify before adding more agents?",
        "options": [
            "A concrete benefit that outweighs coordination, latency, cost, and failure complexity",
            "The need to maximize the number of model calls",
            "A way to avoid evaluating individual components",
            "A guarantee that agents will never disagree",
        ],
        "correct_option": 0,
        "explanation": "Multiple agents add coordination and operational complexity; use them only when the task benefits from the decomposition.",
    },
    {
        "prompt": "Which measurements can help assess agent efficiency and reliability?",
        "options": [
            "Success rate, steps, latency, tool errors, and cost",
            "Only the final response's character count",
            "Only the model's training loss",
            "The number of tools listed in documentation",
        ],
        "correct_option": 0,
        "explanation": "Track outcome quality together with operational measures such as tool errors, number of steps, latency, and cost.",
    },
    {
        "prompt": "Why should an agent have a user-visible stop or cancel mechanism?",
        "options": [
            "It lets users halt a run that is taking too long or acting unexpectedly",
            "It guarantees all side effects are automatically rolled back",
            "It replaces the need for server-side budgets",
            "It forces the model to complete the task successfully",
        ],
        "correct_option": 0,
        "explanation": "A stop control improves user control, though stopping a run does not necessarily roll back actions already completed.",
    },
    {
        "prompt": "Why should the application verify a tool result before reporting success?",
        "options": [
            "A tool can fail, return incomplete data, or report success without satisfying the user's goal",
            "The model cannot receive tool results",
            "Verification makes an audit trail unnecessary",
            "Tools always return false values",
        ],
        "correct_option": 0,
        "explanation": "Check tool status and postconditions so the agent does not claim completion based only on an attempted action.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="agentic-ai",
            defaults={"name": "Agentic AI", "icon": "brain", "order": 180, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="agentic-ai-fundamentals-quiz",
            defaults={
                "title": "Agentic AI Fundamentals Quiz",
                "description": "20 questions covering agent loops, tool design, memory, permissions, evaluation, and operational safety.",
                "category": category,
                "difficulty": Quiz.Difficulty.MEDIUM,
                "time_limit_minutes": 20,
                "show_leaderboard": True,
                "order": 1,
                "is_published": True,
            },
        )
        if quiz.category_id != category.id or not quiz.is_published:
            quiz.category = category
            quiz.is_published = True
            quiz.save(update_fields=["category", "is_published"])

        QuizQuestion.objects.filter(quiz=quiz, order__gt=len(QUESTIONS)).delete()
        for index, question in enumerate(QUESTIONS, start=1):
            QuizQuestion.objects.update_or_create(
                quiz=quiz,
                order=index,
                defaults={
                    "type": QuizQuestion.Type.MCQ,
                    "prompt": question["prompt"],
                    "options": question["options"],
                    "correct_option": question["correct_option"],
                    "explanation": question["explanation"],
                    "points": 1,
                },
            )

    print(f"Category: {category.slug} (published={category.is_published})")
    print(f"Quiz: {quiz.slug} - {quiz.questions.count()} questions")


if __name__ == "__main__":
    run()