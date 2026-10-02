"""Seed the Generative AI category and its 20-question fundamentals quiz.

Usage: python seed_quiz_generative_ai.py (run from backend/, same venv as manage.py)
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
        "prompt": "What does tokenization do in a language model pipeline?",
        "options": [
            "Converts text into token identifiers the model can process",
            "Encrypts text so the model cannot read it",
            "Guarantees each word is one token",
            "Validates whether every statement is true",
        ],
        "correct_option": 0,
        "explanation": "Tokenization maps text into units from a model's vocabulary; a word may map to one or several tokens.",
    },
    {
        "prompt": "What is a model's context window?",
        "options": [
            "The bounded amount of tokenized input and output the model can handle in one request",
            "The number of documents in a vector database",
            "The total disk space used by a model",
            "The number of concurrent users a web server supports",
        ],
        "correct_option": 0,
        "explanation": "The context window limits tokens available to a request, including instructions, conversation, retrieved context, and output.",
    },
    {
        "prompt": "What does increasing temperature generally do when sampling model outputs?",
        "options": [
            "Can make output selection more variable; it does not guarantee greater factual accuracy",
            "Increase the context window",
            "Add citations to every claim",
            "Fine-tune the model's parameters immediately",
        ],
        "correct_option": 0,
        "explanation": "Temperature changes the sampling distribution and can affect variability; it is not a factuality control.",
    },
    {
        "prompt": "What does top-p sampling do?",
        "options": [
            "Samples from a set of likely next tokens whose cumulative probability reaches a threshold",
            "Retrieves the top-p documents from a database",
            "Sets the model's maximum context length",
            "Measures precision of a classifier",
        ],
        "correct_option": 0,
        "explanation": "Nucleus sampling restricts choices to a probability-mass set of likely next tokens before sampling.",
    },
    {
        "prompt": "What are text embeddings commonly used for?",
        "options": [
            "Represent text as vectors for similarity search or other downstream tasks",
            "Prove a document is factually correct",
            "Encrypt a prompt for secure transmission",
            "Replace every authorization check",
        ],
        "correct_option": 0,
        "explanation": "Embeddings map text to numeric vectors that can support semantic similarity search, but similarity is not proof of truth.",
    },
    {
        "prompt": "What is a common trade-off when choosing RAG chunk size?",
        "options": [
            "Small chunks can improve focused retrieval but lose context; large chunks retain context but may add noise",
            "Smaller chunks always guarantee correct answers",
            "Larger chunks eliminate the context window limit",
            "Chunk size determines the model's training data",
        ],
        "correct_option": 0,
        "explanation": "Chunk size affects retrieval granularity and context completeness; choose and evaluate it for the document and task.",
    },
    {
        "prompt": "What does vector similarity search commonly rank?",
        "options": [
            "Vectors by a chosen distance or similarity measure",
            "Documents by their factual accuracy guarantee",
            "Users by authorization level automatically",
            "Prompts by token count only",
        ],
        "correct_option": 0,
        "explanation": "Vector search ranks representations according to a metric such as cosine similarity or distance; relevance still needs evaluation.",
    },
    {
        "prompt": "What is the purpose of retrieval in retrieval-augmented generation?",
        "options": [
            "Find relevant external context to provide to the generator",
            "Guarantee every generated answer is correct",
            "Replace all data access controls",
            "Train a new model for each user question",
        ],
        "correct_option": 0,
        "explanation": "RAG retrieves relevant context to condition generation; poor retrieval or synthesis can still produce unsupported answers.",
    },
    {
        "prompt": "When can hybrid keyword and vector search be useful?",
        "options": [
            "When both semantic similarity and exact terms such as IDs or product codes matter",
            "Only when no documents have text",
            "To avoid evaluating retrieval quality",
            "To guarantee that an LLM never hallucinates",
        ],
        "correct_option": 0,
        "explanation": "Hybrid retrieval can combine semantic matching with lexical matching for exact identifiers and terminology.",
    },
    {
        "prompt": "What does a reranker commonly do in a retrieval pipeline?",
        "options": [
            "Re-score an initial candidate set to improve ordering by relevance",
            "Rewrite the source documents permanently",
            "Replace authentication in the application",
            "Generate vector embeddings without reading text",
        ],
        "correct_option": 0,
        "explanation": "A reranker evaluates retrieved candidates more deeply and can reorder them before context is sent to a generator.",
    },
    {
        "prompt": "What is a hallucination in generative AI?",
        "options": [
            "A plausible-sounding output that is unsupported or incorrect",
            "A model's context window",
            "A successful authorization check",
            "A vector database index type",
        ],
        "correct_option": 0,
        "explanation": "A hallucination is generated content that may sound plausible but is unsupported or false.",
    },
    {
        "prompt": "What is prompt injection?",
        "options": [
            "Untrusted content attempts to override instructions or misuse model capabilities",
            "A method for reducing token count by compression",
            "A guaranteed way to improve retrieval precision",
            "A DAX formula for measures",
        ],
        "correct_option": 0,
        "explanation": "Prompt injection uses untrusted instructions, including those in retrieved content, to influence a model in unintended ways.",
    },
    {
        "prompt": "Why validate structured model output against a schema?",
        "options": [
            "The model can still return malformed or invalid data despite format instructions",
            "Schema validation proves every field is factually correct",
            "It makes user authorization unnecessary",
            "It guarantees no output will contain sensitive data",
        ],
        "correct_option": 0,
        "explanation": "Structured output still needs parsing and validation; schema conformance does not establish truth or authorization.",
    },
    {
        "prompt": "How does fine-tuning differ from RAG at a high level?",
        "options": [
            "Fine-tuning updates model parameters; RAG retrieves context at inference time",
            "RAG always updates model parameters after each question",
            "Fine-tuning only changes the system prompt",
            "They are identical techniques with different APIs",
        ],
        "correct_option": 0,
        "explanation": "Fine-tuning changes learned parameters using training data; RAG supplies retrieved information during a request.",
    },
    {
        "prompt": "What happens in a typical tool-calling workflow?",
        "options": [
            "The model proposes a structured tool call and application code validates and executes it",
            "The model directly gains unrestricted operating-system access",
            "The tool executes without receiving inputs",
            "A tool call guarantees exactly-once side effects",
        ],
        "correct_option": 0,
        "explanation": "Applications interpret proposed calls, validate inputs and permissions, execute approved tools, and return results to the model.",
    },
    {
        "prompt": "Where should authorization for a model-invoked tool be enforced?",
        "options": [
            "In the application or tool backend for each operation",
            "Only in the system prompt",
            "Only by hiding the tool name from the user interface",
            "Only in the model's vector embeddings",
        ],
        "correct_option": 0,
        "explanation": "Authorization must be enforced by trusted application code; prompts and UI restrictions are not security boundaries.",
    },
    {
        "prompt": "Why use a fixed representative evaluation set when changing a prompt or retrieval system?",
        "options": [
            "To compare versions consistently on important cases and failure modes",
            "To guarantee that the next model release will be correct",
            "To replace all production monitoring",
            "To make human review unnecessary",
        ],
        "correct_option": 0,
        "explanation": "A stable evaluation set supports meaningful comparisons, provided it represents actual tasks and is not overfit through repeated tuning.",
    },
    {
        "prompt": "Why evaluate retrieval quality separately from generated answer quality?",
        "options": [
            "A wrong answer may come from poor retrieval or from synthesis despite good retrieved context",
            "Retrieval quality is always identical to answer quality",
            "Only the final answer can be measured",
            "It removes the need to inspect source documents",
        ],
        "correct_option": 0,
        "explanation": "Separating retrieval and generation metrics helps identify which stage causes failures and what to improve.",
    },
    {
        "prompt": "Which operational metrics are useful for a production generative AI feature?",
        "options": [
            "Latency, cost, availability, refusal and failure rates, and quality measures",
            "Only the model's parameter count",
            "Only the number of prompt characters in source control",
            "Only the color of the report dashboard",
        ],
        "correct_option": 0,
        "explanation": "Operational monitoring should cover service health, latency, cost, and task-specific quality and safety behavior.",
    },
    {
        "prompt": "What should a multimodal generative model be evaluated on?",
        "options": [
            "The relevant input and output modalities and their cross-modal failure cases",
            "Text output only in every application",
            "Only the number of model layers",
            "Whether it can replace all accessibility testing",
        ],
        "correct_option": 0,
        "explanation": "Multimodal systems need evaluation appropriate to their inputs and outputs, including errors in cross-modal grounding and interpretation.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="generative-ai",
            defaults={"name": "Generative AI", "icon": "brain", "order": 170, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="generative-ai-fundamentals-quiz",
            defaults={
                "title": "Generative AI Fundamentals Quiz",
                "description": "20 questions covering prompting, tokenization, RAG, tool use, evaluation, and production controls.",
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