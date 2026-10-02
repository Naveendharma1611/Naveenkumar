"""Seed the Git and GitHub category and its 20-question fundamentals quiz.

Usage: python seed_quiz_git_github.py (run from backend/, same venv as manage.py)
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
        "prompt": "What is the Git index (staging area) used for?",
        "options": [
            "Select the content that will be recorded in the next commit",
            "Store all remote repositories permanently",
            "Replace the working tree with a backup",
            "Run GitHub Actions locally",
        ],
        "correct_option": 0,
        "explanation": "The index holds the proposed snapshot for the next commit, allowing you to stage selected changes.",
    },
    {
        "prompt": "What does `git diff --cached` show?",
        "options": [
            "Differences between the index and the current commit",
            "Only untracked files in every remote branch",
            "The contents of the latest GitHub issue",
            "Changes between two repositories that have no common history only",
        ],
        "correct_option": 0,
        "explanation": "`git diff --cached` reviews staged changes relative to the current commit.",
    },
    {
        "prompt": "What is a Git branch?",
        "options": [
            "A lightweight movable reference to a commit",
            "A complete duplicate copy of the repository files",
            "A remote server account",
            "A list of staged files",
        ],
        "correct_option": 0,
        "explanation": "A branch is a movable reference that advances as commits are made on that line of development.",
    },
    {
        "prompt": "What does `git fetch origin` do by itself?",
        "options": [
            "Downloads remote objects and updates remote-tracking references without integrating them into the current branch",
            "Always merges the remote main branch into the current branch",
            "Deletes all local branches",
            "Pushes local commits to the remote",
        ],
        "correct_option": 0,
        "explanation": "Fetch updates the local view of the remote but does not merge or rebase changes into the checked-out branch.",
    },
    {
        "prompt": "What does `git pull` generally do?",
        "options": [
            "Fetches from a remote and then integrates changes according to configuration",
            "Only displays the current branch name",
            "Creates a new GitHub repository automatically",
            "Deletes every untracked file before fetching",
        ],
        "correct_option": 0,
        "explanation": "Pull combines fetching with integration, commonly by merge or rebase depending on configuration.",
    },
    {
        "prompt": "How do merge and rebase generally differ?",
        "options": [
            "Merge combines histories; rebase replays commits on a new base and creates new commit IDs",
            "Merge always deletes a branch; rebase always preserves every commit ID",
            "Rebase fetches files but merge stages them",
            "They are identical commands with different names",
        ],
        "correct_option": 0,
        "explanation": "Merge preserves branch histories; rebase replays commits, rewriting their IDs, so shared history requires coordination.",
    },
    {
        "prompt": "Which command is generally appropriate for undoing a commit already shared with collaborators?",
        "options": ["`git revert <commit>`", "`git reset --hard <commit>`", "`git clean -fd`", "`git branch -D main`"],
        "correct_option": 0,
        "explanation": "Revert creates a new inverse commit without rewriting the shared history.",
    },
    {
        "prompt": "What does `git restore --staged file` do?",
        "options": [
            "Unstages the path while keeping its working-tree edits",
            "Deletes the file from disk permanently",
            "Commits the file automatically",
            "Removes the file from every remote branch",
        ],
        "correct_option": 0,
        "explanation": "This restores the index entry from HEAD and leaves the working-tree contents in place.",
    },
    {
        "prompt": "Does adding an already tracked file to `.gitignore` stop Git from tracking it?",
        "options": ["No", "Yes, immediately and permanently", "Only after a pull request", "Only when the file is empty"],
        "correct_option": 0,
        "explanation": "Ignore rules apply to untracked files; a tracked file remains tracked until explicitly removed from the index in a commit.",
    },
    {
        "prompt": "What should you do first if an access token is accidentally committed?",
        "options": [
            "Revoke or rotate the token immediately",
            "Only add its filename to `.gitignore`",
            "Wait until the next release to delete it",
            "Rename the local branch",
        ],
        "correct_option": 0,
        "explanation": "A later deletion does not invalidate an exposed credential; revoke or rotate it first, then assess history cleanup.",
    },
    {
        "prompt": "What is a GitHub pull request commonly used for?",
        "options": [
            "Propose, discuss, review, and check changes before integrating a branch",
            "Replace the local Git repository",
            "Store a user's password in source history",
            "Run a SQL query against every contributor's machine",
        ],
        "correct_option": 0,
        "explanation": "Pull requests provide a collaboration and review workflow for proposed changes.",
    },
    {
        "prompt": "What can branch protection require before changes merge?",
        "options": [
            "Reviews and passing status checks",
            "Every contributor to delete their local repository",
            "All commit messages to be identical",
            "A force push from an administrator",
        ],
        "correct_option": 0,
        "explanation": "Branch rules can require pull requests, approvals, status checks, or other gates; bypass permissions should also be controlled.",
    },
    {
        "prompt": "What is continuous integration (CI) commonly used for?",
        "options": [
            "Run repeatable checks such as tests, linting, or builds on repository events",
            "Guarantee software has no defects",
            "Replace code review and testing design",
            "Automatically rewrite every contributor's branch history",
        ],
        "correct_option": 0,
        "explanation": "CI automates repeatable validation and provides evidence about a change, but does not prove correctness.",
    },
    {
        "prompt": "Why should a GitHub Actions workflow use least-privilege token permissions?",
        "options": [
            "To limit the impact if a workflow step or dependency is compromised",
            "To make every job run as an administrator",
            "To expose repository secrets in pull-request logs",
            "To disable all status checks",
        ],
        "correct_option": 0,
        "explanation": "Limiting permissions reduces what compromised automation can read or change.",
    },
    {
        "prompt": "What does a Git tag commonly identify?",
        "options": ["A specific commit, often used to mark a release", "The current staging area only", "A pull request reviewer", "Every file ignored by Git"],
        "correct_option": 0,
        "explanation": "A tag is a named reference to a commit and is commonly used to identify releases.",
    },
    {
        "prompt": "What is a detached HEAD state?",
        "options": [
            "HEAD points directly to a commit rather than a branch",
            "The repository has no commits",
            "The index and working tree are always empty",
            "A remote server has disconnected permanently",
        ],
        "correct_option": 0,
        "explanation": "Commits can be created while detached, but they are not automatically attached to a named branch.",
    },
    {
        "prompt": "Why is blindly choosing “ours” or “theirs” risky when resolving a merge conflict?",
        "options": [
            "The correct resolution may need to combine both intended changes or use a different design",
            "Git forbids staging a resolved conflict",
            "Conflict markers become valid source code",
            "The merge always restarts from the initial commit",
        ],
        "correct_option": 0,
        "explanation": "A conflict is a semantic decision; inspect both changes, create the intended result, and test it.",
    },
    {
        "prompt": "What does `git stash` commonly do?",
        "options": [
            "Temporarily saves local changes so the working tree can be switched or cleaned up",
            "Publishes changes to GitHub",
            "Creates a release tag",
            "Deletes all commits after HEAD",
        ],
        "correct_option": 0,
        "explanation": "Stash saves selected local changes for later reapplication; inspect the result when applying it again.",
    },
    {
        "prompt": "What does `git push -u origin feature/name` configure on the first push?",
        "options": [
            "An upstream tracking relationship for the local branch",
            "A protected branch rule on GitHub",
            "A new tag at the current commit",
            "A merge from origin into the local branch",
        ],
        "correct_option": 0,
        "explanation": "The `-u` option sets the upstream so later pull and push commands can infer the tracking branch.",
    },
    {
        "prompt": "What does `git reset --soft <commit>` do to the index and working tree?",
        "options": [
            "Moves HEAD while leaving changes staged",
            "Deletes all tracked and untracked files",
            "Creates a new commit that reverses the target",
            "Only downloads remote history",
        ],
        "correct_option": 0,
        "explanation": "Soft reset moves the current branch reference but keeps the index and working tree at their current content.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="git-github",
            defaults={"name": "Git and GitHub", "icon": "code", "order": 29, "is_published": True},
        )
        if category.name != "Git and GitHub" or not category.is_published:
            category.name = "Git and GitHub"
            category.is_published = True
            category.save(update_fields=["name", "is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="git-github-fundamentals-quiz",
            defaults={
                "title": "Git and GitHub Fundamentals Quiz",
                "description": "20 questions covering Git snapshots, branches, remotes, recovery, pull requests, security, and CI.",
                "category": category,
                "difficulty": Quiz.Difficulty.EASY,
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