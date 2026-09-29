from django.core.cache import cache
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User
from apps.projects.models import Project
from apps.quizzes.models import Quiz, QuizQuestion

from .models import Course, Lesson, StudyCategory


class LearningTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.category = StudyCategory.objects.create(name="Python")
        self.course = Course.objects.create(category=self.category, title="Python Basics", is_published=True)
        self.l1 = Lesson.objects.create(course=self.course, title="Variables", order=1, is_published=True)
        self.l2 = Lesson.objects.create(course=self.course, title="Loops", order=2, is_published=True)
        self.draft = Lesson.objects.create(course=self.course, title="Draft", order=3, is_published=False)
        self.student = User.objects.create_user("s@example.com", "Str0ng-Passw0rd!", full_name="Sam S", role=Role.STUDENT)
        self.visitor = User.objects.create_user("v@example.com", "Str0ng-Passw0rd!", full_name="Val V", role=Role.VISITOR)

    def test_lesson_slug_scoped_to_category(self):
        sql = StudyCategory.objects.create(name="SQL")
        sql_course = Course.objects.create(category=sql, title="SQL Basics", is_published=True)
        other = Lesson.objects.create(course=sql_course, title="Variables", is_published=True)
        self.assertEqual(other.slug, "variables")
        dup = Lesson.objects.create(course=self.course, title="Variables", is_published=True)
        self.assertEqual(dup.slug, "variables-2")

    def test_lesson_by_slug_with_navigation_and_drafts_hidden(self):
        res = self.client.get("/api/study/lesson/python/variables/")
        self.assertEqual(res.status_code, 200)
        self.assertIsNone(res.data["previous"])
        self.assertEqual(res.data["next"]["slug"], "loops")
        self.assertIsNone(res.data["user_state"])
        self.assertEqual(self.client.get("/api/study/lesson/python/draft/").status_code, 404)
        self.assertIsNone(self.client.get("/api/study/lesson/python/loops/").data["next"])

    def test_category_detail_lists_published_lessons_only(self):
        res = self.client.get("/api/study/categories/python/")
        titles = [lesson["title"] for lesson in res.data["courses"][0]["lessons"]]
        self.assertEqual(titles, ["Variables", "Loops"])

    def test_progress_bookmark_note_and_dashboard(self):
        self.client.force_authenticate(self.student)
        self.assertEqual(self.client.post("/api/study/progress/", {"lesson": self.l1.id}).status_code, 200)
        self.assertTrue(self.client.post("/api/study/bookmarks/", {"lesson": self.l1.id}).data["bookmarked"])
        self.assertEqual(self.client.put("/api/study/notes/", {"lesson": self.l1.id, "content": "hi"}).status_code, 200)
        state = self.client.get("/api/study/lesson/python/variables/").data["user_state"]
        self.assertEqual(state, {"completed": True, "bookmarked": True, "note": "hi"})

        dash = self.client.get("/api/student/dashboard/").data
        self.assertEqual(dash["lessons_completed"], 1)
        self.assertEqual(dash["category_progress"][0]["percent"], 50)
        self.assertEqual(dash["courses_completed"], 0)

        # cannot mark unpublished lessons
        self.assertEqual(self.client.post("/api/study/progress/", {"lesson": self.draft.id}).status_code, 400)

    def test_visitors_and_anonymous_cannot_track_progress(self):
        self.assertEqual(self.client.post("/api/study/progress/", {"lesson": self.l1.id}).status_code, 401)
        self.client.force_authenticate(self.visitor)
        self.assertEqual(self.client.post("/api/study/progress/", {"lesson": self.l1.id}).status_code, 403)
        self.assertEqual(self.client.get("/api/student/dashboard/").status_code, 403)

    def test_public_cannot_write_content(self):
        res = self.client.post("/api/study/categories/", {"name": "Hack"})
        self.assertEqual(res.status_code, 401)
        self.client.force_authenticate(self.student)
        self.assertEqual(self.client.post("/api/study/categories/", {"name": "Hack"}).status_code, 403)

    def test_global_search(self):
        Project.objects.create(title="Loop Detector", category="PYTHON", summary="x", is_published=True)
        res = self.client.get("/api/search/?q=loop")
        types = {g["type"] for g in res.data["groups"]}
        self.assertEqual(types, {"projects", "lessons"})


class QuizTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.quiz = Quiz.objects.create(title="Python Basics Quiz", is_published=True, time_limit_minutes=5)
        self.mcq = QuizQuestion.objects.create(
            quiz=self.quiz, type="MCQ", prompt="Mutable?", options=["tuple", "list"], correct_option=1
        )
        self.output = QuizQuestion.objects.create(
            quiz=self.quiz, type="OUTPUT", prompt="print(2**3)", accepted_answers=["8"], points=2
        )
        self.theory = QuizQuestion.objects.create(quiz=self.quiz, type="THEORY", prompt="Explain GIL")
        self.student = User.objects.create_user("s@example.com", "x", full_name="Sam Student", role=Role.STUDENT)

    def test_detail_hides_answers(self):
        res = self.client.get(f"/api/quizzes/{self.quiz.slug}/")
        self.assertEqual(res.data["question_count"], 3)
        self.assertNotIn("correct_option", res.data["questions"][0])
        self.assertNotIn("accepted_answers", res.data["questions"][1])

    def test_anonymous_submit_is_graded_not_saved(self):
        res = self.client.post(f"/api/quizzes/{self.quiz.slug}/submit/", {
            "answers": {str(self.mcq.id): "1", str(self.output.id): " 8 "},
        }, format="json")
        self.assertEqual((res.data["score"], res.data["max_score"], res.data["percent"]), (3, 3, 100))
        self.assertFalse(res.data["saved"])
        theory = next(r for r in res.data["results"] if r["question_id"] == self.theory.id)
        self.assertIsNone(theory["correct"])

    def test_student_attempt_saved_and_leaderboard(self):
        self.client.force_authenticate(self.student)
        attempt_id = self.client.post(f"/api/quizzes/{self.quiz.slug}/start/").data["attempt_id"]
        res = self.client.post(f"/api/quizzes/{self.quiz.slug}/submit/", {
            "attempt_id": attempt_id, "answers": {str(self.mcq.id): "0", str(self.output.id): "8"},
        }, format="json")
        self.assertTrue(res.data["saved"])
        self.assertEqual(res.data["percent"], 67)
        board = self.client.get(f"/api/quizzes/{self.quiz.slug}/leaderboard/").data
        self.assertEqual(board, [{"rank": 1, "name": "Sam", "percent": 67}])
        # attempt cannot be submitted twice
        again = self.client.post(f"/api/quizzes/{self.quiz.slug}/submit/", {
            "attempt_id": attempt_id, "answers": {},
        }, format="json")
        self.assertEqual(again.status_code, 404)


class ContactTests(APITestCase):
    def setUp(self):
        cache.clear()

    def test_contact_saves_real_messages_and_drops_bots(self):
        from apps.contact.models import ContactMessage

        payload = {"name": "Ann", "email": "ann@example.com", "subject": "Hi", "message": "Hello there, nice site!"}
        self.assertEqual(self.client.post("/api/contact/", {**payload, "elapsed_ms": 8000}).status_code, 201)
        self.assertEqual(self.client.post("/api/contact/", {**payload, "website": "spam.com"}).status_code, 201)
        self.assertEqual(self.client.post("/api/contact/", {**payload, "elapsed_ms": 200}).status_code, 201)
        self.assertEqual(ContactMessage.objects.count(), 1)
