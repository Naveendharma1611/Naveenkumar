import re

from django.core import mail
from django.core.cache import cache
from rest_framework.test import APITestCase

from .models import Role, User

STRONG = "Str0ng-Passw0rd!"


class AuthFlowTests(APITestCase):
    def setUp(self):
        cache.clear()  # reset throttle counters between tests

    def register(self, role="STUDENT", email="student@example.com"):
        return self.client.post(
            "/api/auth/register/",
            {"email": email, "full_name": "Test Student", "role": role, "password": STRONG, "password_confirm": STRONG},
        )

    def test_student_registration_creates_profile_and_returns_tokens(self):
        res = self.register()
        self.assertEqual(res.status_code, 201, res.data)
        self.assertEqual(res.data["user"]["role"], "STUDENT")
        self.assertIn("access", res.data)
        user = User.objects.get(email="student@example.com")
        self.assertTrue(hasattr(user, "student_profile"))
        self.assertNotEqual(user.password, STRONG)  # hashed

    def test_visitor_registration(self):
        res = self.register(role="VISITOR", email="visitor@example.com")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["user"]["role"], "VISITOR")

    def test_cannot_self_register_as_admin(self):
        res = self.register(role="ADMIN")
        self.assertEqual(res.status_code, 400)
        self.assertIn("role", res.data["errors"])

    def test_password_mismatch_and_weak_password_rejected(self):
        res = self.client.post("/api/auth/register/", {
            "email": "a@example.com", "full_name": "A B", "password": STRONG, "password_confirm": "other",
        })
        self.assertEqual(res.status_code, 400)
        res = self.client.post("/api/auth/register/", {
            "email": "a@example.com", "full_name": "A B", "password": "123", "password_confirm": "123",
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("password", res.data["errors"])

    def test_duplicate_email_rejected_case_insensitive(self):
        self.register()
        res = self.register(email="STUDENT@example.com")
        self.assertEqual(res.status_code, 400)

    def test_login_me_logout(self):
        self.register()
        res = self.client.post("/api/auth/login/", {"email": "Student@Example.com", "password": STRONG})
        self.assertEqual(res.status_code, 200, res.data)
        access, refresh = res.data["access"], res.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(self.client.get("/api/auth/me/").data["email"], "student@example.com")
        self.client.credentials()
        self.assertEqual(self.client.post("/api/auth/logout/", {"refresh": refresh}).status_code, 204)
        self.assertEqual(self.client.post("/api/auth/refresh/", {"refresh": refresh}).status_code, 401)

    def test_login_wrong_password(self):
        self.register()
        res = self.client.post("/api/auth/login/", {"email": "student@example.com", "password": "nope"})
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data["detail"], "Invalid email or password.")

    def test_password_reset_flow(self):
        self.register()
        res = self.client.post("/api/auth/password-reset/", {"email": "student@example.com"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        uid, token = re.search(r"uid=([^&]+)&token=(\S+)", mail.outbox[0].body).groups()
        new = "An0ther-Strong-Pass"
        res = self.client.post("/api/auth/password-reset/confirm/", {"uid": uid, "token": token, "new_password": new})
        self.assertEqual(res.status_code, 200, res.data)
        self.assertEqual(self.client.post("/api/auth/login/", {"email": "student@example.com", "password": new}).status_code, 200)
        # token is single-use
        res = self.client.post("/api/auth/password-reset/confirm/", {"uid": uid, "token": token, "new_password": new})
        self.assertEqual(res.status_code, 400)

    def test_password_reset_unknown_email_does_not_leak(self):
        res = self.client.post("/api/auth/password-reset/", {"email": "nobody@example.com"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_visitor_upgrade_to_student(self):
        access = self.register(role="VISITOR", email="v@example.com").data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        res = self.client.post("/api/auth/upgrade-to-student/")
        self.assertEqual(res.data["user"]["role"], "STUDENT")

    def test_admin_endpoints_require_admin(self):
        access = self.register().data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(self.client.get("/api/admin/users/").status_code, 403)
        admin = User.objects.create_superuser("admin@example.com", STRONG, full_name="Admin")
        self.assertEqual(admin.role, Role.ADMIN)
        token = self.client.post("/api/auth/login/", {"email": "admin@example.com", "password": STRONG}).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(self.client.get("/api/admin/users/").status_code, 200)
        self.assertEqual(self.client.get("/api/admin/overview/").status_code, 200)
