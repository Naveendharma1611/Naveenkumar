"""Seed the DSA category and its 20-question fundamentals quiz.

Usage: python seed_quiz_dsa.py (run from backend/, same venv as manage.py)
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
        "prompt": "What does `O(n)` time complexity describe?",
        "options": [
            "Work that grows linearly with input size asymptotically",
            "An exact runtime of n seconds",
            "Constant memory use for every algorithm",
            "An algorithm that always performs n comparisons",
        ],
        "correct_option": 0,
        "explanation": "Big O describes asymptotic growth, not an exact runtime; constants and lower-order terms are omitted.",
    },
    {
        "prompt": "What is the time complexity of binary search on a sorted array?",
        "options": ["`O(log n)`", "`O(n)`", "`O(n log n)`", "`O(1)` in every case"],
        "correct_option": 0,
        "explanation": "Each comparison discards about half of the remaining search interval, giving logarithmic time.",
    },
    {
        "prompt": "After `O(n)` prefix-sum preprocessing, what is the cost of a range-sum query using two prefix values?",
        "options": ["`O(1)`", "`O(log n)`", "`O(n)`", "`O(n log n)`"],
        "correct_option": 0,
        "explanation": "A half-open range sum is the difference between two prefix entries, requiring constant work.",
    },
    {
        "prompt": "What is the expected lookup time for a hash set under typical hashing assumptions?",
        "options": ["`O(1)`", "`O(log n)`", "`O(n)` always", "`O(n^2)`"],
        "correct_option": 0,
        "explanation": "Hash set membership is expected `O(1)` under typical assumptions, though worst-case behavior can be linear.",
    },
    {
        "prompt": "What is the cost of accessing the item at index `i` in a singly linked list?",
        "options": ["`O(n)` in general", "`O(1)` by index", "`O(log n)` by index", "`O(n log n)`"],
        "correct_option": 0,
        "explanation": "A linked list must follow links from an endpoint to reach an indexed position, which takes linear time in general.",
    },
    {
        "prompt": "Which abstract data type removes the most recently added item first?",
        "options": ["Stack", "Queue", "Priority queue only", "Disjoint-set union"],
        "correct_option": 0,
        "explanation": "A stack is last-in, first-out (LIFO).",
    },
    {
        "prompt": "When does BFS find a path with the fewest edges?",
        "options": [
            "In an unweighted graph, or one where every edge has equal weight",
            "In every graph with arbitrary negative weights",
            "Only in a directed acyclic graph",
            "Only when the graph is a complete graph",
        ],
        "correct_option": 0,
        "explanation": "BFS explores by number of edges from the source, so it finds shortest paths in unweighted graphs.",
    },
    {
        "prompt": "How much space does an adjacency-list representation of a graph typically use?",
        "options": ["`O(V + E)`", "`O(V^2)` in every graph", "`O(E^2)`", "`O(log V)`"],
        "correct_option": 0,
        "explanation": "An adjacency list stores vertices and their incident edges, using space proportional to `V + E`.",
    },
    {
        "prompt": "What precondition does ordinary binary search rely on?",
        "options": [
            "The searched values are sorted or the tested predicate is monotonic",
            "The array has no duplicate values",
            "The array length is a power of two",
            "Every value is positive",
        ],
        "correct_option": 0,
        "explanation": "Binary search can discard half the interval only when ordering or a monotonic predicate justifies that decision.",
    },
    {
        "prompt": "What does a stable sorting algorithm preserve?",
        "options": [
            "The relative order of records with equal sort keys",
            "The input array's original memory address",
            "The order of values regardless of the sort key",
            "Constant-time insertion for all data",
        ],
        "correct_option": 0,
        "explanation": "Stability means equal-key items retain their input relative order.",
    },
    {
        "prompt": "What is the typical time complexity of finding the top `k` values with a size-`k` heap while scanning `n` values?",
        "options": ["`O(n log k)`", "`O(k^n)`", "`O(log n)` total", "`O(n^2)` always"],
        "correct_option": 0,
        "explanation": "Maintaining a bounded heap takes `O(log k)` for relevant updates across `n` input values.",
    },
    {
        "prompt": "What is the worst-case search time in an unbalanced binary search tree with `n` nodes?",
        "options": ["`O(n)`", "`O(1)`", "`O(log n)` guaranteed", "`O(n log n)`"],
        "correct_option": 0,
        "explanation": "An unbalanced BST can become a chain with height `n`, so operations can take linear time.",
    },
    {
        "prompt": "What value is at the root of a min-heap?",
        "options": ["A minimum value among the heap elements", "The median value", "The most recently inserted value", "The maximum value by definition"],
        "correct_option": 0,
        "explanation": "A min-heap guarantees its smallest element at the root, but does not fully sort all remaining elements.",
    },
    {
        "prompt": "What edge-weight condition is required for standard Dijkstra shortest-path reasoning?",
        "options": ["All edge weights are nonnegative", "All edge weights are negative", "The graph must be unweighted", "Every vertex must have degree two"],
        "correct_option": 0,
        "explanation": "Dijkstra's algorithm relies on nonnegative edge weights; negative edges can invalidate its greedy finalization step.",
    },
    {
        "prompt": "When does a directed graph have a topological ordering?",
        "options": ["When it is acyclic", "Only when it is complete", "Only when every edge is bidirectional", "Whenever it has a self-loop"],
        "correct_option": 0,
        "explanation": "A directed acyclic graph (DAG) has a topological order; a directed cycle prevents one.",
    },
    {
        "prompt": "What does disjoint-set union efficiently support?",
        "options": [
            "Merging components and checking whether elements share a component",
            "Finding shortest paths with arbitrary negative edges",
            "Sorting a list of strings lexicographically",
            "Returning every subarray sum in constant space",
        ],
        "correct_option": 0,
        "explanation": "Union-find supports union and find operations for connectivity among disjoint sets.",
    },
    {
        "prompt": "What is needed to justify a greedy algorithm?",
        "options": [
            "A correctness argument showing local choices can lead to an optimal solution",
            "One example where the algorithm returns a good answer",
            "A faster computer than the brute-force method",
            "A sorted input in every possible problem",
        ],
        "correct_option": 0,
        "explanation": "Greedy correctness needs a proof, such as an exchange argument or greedy-choice property, not only examples.",
    },
    {
        "prompt": "Which properties commonly indicate a dynamic-programming approach may help?",
        "options": [
            "Overlapping subproblems and an answer composed from smaller subproblems",
            "A requirement to sort every input first",
            "A graph with no vertices",
            "A need to store all possible permutations explicitly",
        ],
        "correct_option": 0,
        "explanation": "Dynamic programming is useful when subproblems repeat and a larger solution can be built from smaller states.",
    },
    {
        "prompt": "What is backtracking?",
        "options": [
            "Explore choices, reject invalid partial states, and undo choices to try alternatives",
            "A stable in-place sorting algorithm",
            "A hash collision resolution strategy only",
            "A binary-search boundary convention",
        ],
        "correct_option": 0,
        "explanation": "Backtracking searches a decision tree and prunes partial candidates that cannot lead to valid solutions.",
    },
    {
        "prompt": "Why does a two-pointer pair-sum algorithm commonly require sorted input?",
        "options": [
            "Ordering tells which pointer to move when the current sum is too small or too large",
            "Sorting makes every pair equal to the target",
            "Two pointers can only store positive values",
            "It removes the need to compare values",
        ],
        "correct_option": 0,
        "explanation": "Sorted order justifies moving the left pointer up for a small sum or the right pointer down for a large sum.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="dsa",
            defaults={"name": "Data Structures and Algorithms", "icon": "code", "order": 25, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="dsa-fundamentals-quiz",
            defaults={
                "title": "Data Structures & Algorithms Fundamentals Quiz",
                "description": "20 questions covering complexity, core data structures, searching, graphs, greedy methods, and dynamic programming.",
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