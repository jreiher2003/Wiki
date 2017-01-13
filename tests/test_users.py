import unittest 
from base import BaseTestCase 
from app import app, db 
from app.models import User 
from flask.ext.login import current_user 

class TestLogin(BaseTestCase):

    def test_index(self):
        response = self.client.get("/login", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_correct_login(self):
        response = self.client.post("/login", data=dict(username="Admin", password="password", ip="127.0.0.1"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have signed in as <strong>Admin</strong>!", response.data)

    def test_incorrect_login(self):
        response = self.client.post("/login", data=dict(username="wrong", password="wrong", ip="127.0.0.1"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<strong>Invalid password.</strong> Please try again.", response.data)

    def test_blank_login(self):
        response = self.client.post("/login", data=dict(username="", password=""), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required.", response.data)
        self.assertIn(b"This field is required.", response.data)


    def test_logout(self):
        response = self.client.post("/login", data=dict(username="Admin", password="password", ip="127.0.0.1"), follow_redirects=True)
        response1 = self.client.get("/logout", headers={"Referer": "/login"}, follow_redirects=True)
        self.assertIn(b"You have logged out.", response1.data)

    def test_logout_pre(self):
        response = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You need to login first!", response.data)

    def test_user_signup(self):
        with self.client:
            response = self.client.post("/signup", data=dict(username="Testname", email="test@test.com", password="password", confirm="password"), follow_redirects=True)
            self.assertIn(b"You just added user <strong>Testname</strong>", response.data)
            self.assertTrue(current_user.name == "Testname")
            self.assertTrue(current_user.is_active())
            user = User.query.filter_by(email="test@test.com").first()
            self.assertTrue(str(user) == "<name> Testname")

    def test_incorrect_user_signup(self):
        with self.client:
            response = self.client.post("/signup", data=dict(username="M", email="mi",password="pyth", confirm="python"), follow_redirects=True)
            self.assertIn(b"Field must be between 3 and 25 characters long.", response.data)
            self.assertIn(b"Invalid email address.", response.data)
            self.assertIn(b"Field must be between 6 and 40 characters long.", response.data)
            self.assertIn(b"Field must be between 6 and 25 characters long.", response.data)
            self.assertIn(b"Passwords didn&#39;t match.", response.data)