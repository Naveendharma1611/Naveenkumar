"""Seed the DBMS category and its 20-question fundamentals quiz.

Usage: python seed_quiz_dbms.py (run from backend/, same venv as manage.py)
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
        "prompt": "What is the difference between a database and a DBMS?",
        "options": [
            "A database is organized data; a DBMS is software that manages, protects, and recovers it",
            "A database is a query language; a DBMS is a table",
            "They are exactly the same term",
            "A DBMS is only a backup file",
        ],
        "correct_option": 0,
        "explanation": "The database is the data collection; the DBMS is the system responsible for defining, storing, querying, and protecting it.",
    },
    {
        "prompt": "Which level in the three-schema architecture describes the logical database structure?",
        "options": ["Conceptual level", "External level", "Internal level", "Network transport level"],
        "correct_option": 0,
        "explanation": "The conceptual level describes entities, relationships, and logical constraints independent of physical storage.",
    },
    {
        "prompt": "What is a candidate key?",
        "options": [
            "A minimal set of attributes that uniquely identifies each row",
            "Any attribute that may contain duplicate values",
            "A foreign key that points to any table",
            "A query plan chosen by the optimizer",
        ],
        "correct_option": 0,
        "explanation": "A candidate key uniquely identifies tuples and is minimal; one candidate is selected as the primary key.",
    },
    {
        "prompt": "What does a foreign key constraint help enforce?",
        "options": [
            "Referential integrity between related relations",
            "A particular sort order for all query results",
            "Encryption of every database page",
            "That every table uses a B-tree index",
        ],
        "correct_option": 0,
        "explanation": "A foreign key constrains references to valid related key values, according to the DBMS's constraint rules.",
    },
    {
        "prompt": "What does the functional dependency `X → Y` state?",
        "options": [
            "Equal X values determine equal Y values in the relation",
            "X and Y must be stored in separate databases",
            "Y uniquely determines X in every case",
            "X and Y are always independent variables",
        ],
        "correct_option": 0,
        "explanation": "A functional dependency states that the determinant X uniquely determines the value of Y within the relation.",
    },
    {
        "prompt": "What kind of dependency does Second Normal Form address for a composite candidate key?",
        "options": [
            "A non-prime attribute depending on only part of the key",
            "A foreign key referencing a missing table",
            "Every possible transitive dependency",
            "A query depending on an index",
        ],
        "correct_option": 0,
        "explanation": "2NF requires 1NF and removes partial dependencies of non-prime attributes on a proper subset of a candidate key.",
    },
    {
        "prompt": "What determinant condition defines BCNF?",
        "options": [
            "Every nontrivial functional dependency has a superkey as its determinant",
            "Every table must contain exactly one column",
            "Every relation must have no candidate keys",
            "Every query must use an index",
        ],
        "correct_option": 0,
        "explanation": "BCNF requires every determinant of a nontrivial functional dependency to be a superkey.",
    },
    {
        "prompt": "What does transaction atomicity mean?",
        "options": [
            "The transaction's logical operations commit together or roll back together",
            "Every query executes in constant time",
            "Concurrent transactions never interact",
            "Committed data is always stored in memory only",
        ],
        "correct_option": 0,
        "explanation": "Atomicity is the all-or-nothing property of a transaction.",
    },
    {
        "prompt": "What is a dirty read?",
        "options": [
            "Reading data written by a transaction that has not committed",
            "Reading the same committed row twice",
            "Reading a row with an index",
            "Reading a value from a backup",
        ],
        "correct_option": 0,
        "explanation": "A dirty read observes uncommitted data that may later be rolled back.",
    },
    {
        "prompt": "What is a phantom read?",
        "options": [
            "A repeated predicate query returns a changed set of matching rows",
            "The same row's value changes between reads",
            "A transaction reads uncommitted data only",
            "An index points to a missing file",
        ],
        "correct_option": 0,
        "explanation": "A phantom occurs when a repeated range or predicate query sees a changed set of rows, for example after a matching insert.",
    },
    {
        "prompt": "What does serializability guarantee about concurrent transactions?",
        "options": [
            "Their outcome is equivalent to some serial ordering of those transactions",
            "Every transaction runs on a separate physical server",
            "All queries return the same number of rows",
            "No transaction ever waits for a lock",
        ],
        "correct_option": 0,
        "explanation": "Serializability means concurrent execution is equivalent in outcome to a valid serial ordering.",
    },
    {
        "prompt": "How does MVCC commonly reduce reader-writer blocking?",
        "options": [
            "Readers can access an appropriate row version while writers create newer versions",
            "It disables all transaction isolation",
            "It prevents every write from committing",
            "It stores every query result forever",
        ],
        "correct_option": 0,
        "explanation": "Multi-Version Concurrency Control maintains versions so readers can often use a consistent snapshot while writers proceed.",
    },
    {
        "prompt": "What is a deadlock?",
        "options": [
            "A cycle of transactions waiting on resources held by one another",
            "A query that returns zero rows",
            "An index with no leaf pages",
            "A transaction that has already committed",
        ],
        "correct_option": 0,
        "explanation": "A deadlock is a circular wait; a DBMS can detect the cycle and abort a transaction to break it.",
    },
    {
        "prompt": "Which query pattern is a B-tree index commonly suited to support?",
        "options": ["Ordered range lookup", "Only arbitrary graph traversal", "Only full-table deletion", "Only equality on every unindexed column"],
        "correct_option": 0,
        "explanation": "B-tree indexes maintain ordered keys and commonly support equality, ordering, and range access patterns.",
    },
    {
        "prompt": "For a composite index on `(a, b)`, which predicate commonly benefits from its leftmost prefix?",
        "options": ["A predicate on `a`", "A predicate on `b` only in every DBMS", "A predicate on an unrelated column", "No predicates can use composite indexes"],
        "correct_option": 0,
        "explanation": "A composite B-tree index commonly supports predicates beginning with its leading column; exact optimizer behavior depends on the DBMS and query.",
    },
    {
        "prompt": "What is the write-ahead rule in write-ahead logging?",
        "options": [
            "Required log information is persisted before corresponding data pages are considered safely written",
            "Data pages are always written before any log record exists",
            "Every read must create a backup file",
            "The transaction log is deleted before commit",
        ],
        "correct_option": 0,
        "explanation": "Write-ahead logging requires relevant log records to be persisted before related data pages are safely persisted, supporting recovery.",
    },
    {
        "prompt": "Why is replication not a complete replacement for backups?",
        "options": [
            "Accidental deletion or corruption can propagate to replicas",
            "Replicas can never be used for reads",
            "Replication stores no data",
            "A backup cannot be restored to another server",
        ],
        "correct_option": 0,
        "explanation": "Replication can improve availability but may copy logical errors; retained backups and tested restores protect recovery options.",
    },
    {
        "prompt": "What is sharding?",
        "options": [
            "Partitioning records across multiple nodes or storage partitions",
            "Copying every record to one table in one file only",
            "Adding a B-tree index to every column",
            "Compressing a transaction log",
        ],
        "correct_option": 0,
        "explanation": "Sharding distributes partitions of data across nodes, and shard-key choice affects distribution and query cost.",
    },
    {
        "prompt": "What does CAP discuss during a network partition?",
        "options": [
            "The inability to guarantee both linearizable consistency and availability for every request",
            "A permanent choice of exactly two properties in all conditions",
            "The relation between indexes and normalization",
            "The number of columns allowed in a table",
        ],
        "correct_option": 0,
        "explanation": "CAP describes a trade-off during partitions between availability and linearizable consistency; it is not a blanket statement about normal operation.",
    },
    {
        "prompt": "What is the difference between RPO and RTO?",
        "options": [
            "RPO is the acceptable data-loss window; RTO is the target time to restore service",
            "RPO is query latency; RTO is index size",
            "RPO is the number of replicas; RTO is the number of shards",
            "They are two names for a transaction's isolation level",
        ],
        "correct_option": 0,
        "explanation": "Recovery Point Objective bounds acceptable data loss; Recovery Time Objective sets a target for restoring service.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="dbms",
            defaults={"name": "Database Management Systems", "icon": "database", "order": 26, "is_published": True},
        )
        if category.name != "Database Management Systems" or not category.is_published:
            category.name = "Database Management Systems"
            category.is_published = True
            category.save(update_fields=["name", "is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="dbms-fundamentals-quiz",
            defaults={
                "title": "DBMS Fundamentals Quiz",
                "description": "20 questions covering data models, normalization, transactions, concurrency, recovery, indexing, and distributed systems.",
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