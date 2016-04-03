import unittest 
from base import BaseTestCase 
from app.utils import get_ip

class TestFront(BaseTestCase):

    def test_index_front(self):
        response = self.client.get("/",content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"testpage", response.data)
        self.assertIn(b"test wiki post", response.data)

    def test_wiki_page(self):
        response = self.client.get("/testpage", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"testpage", response.data)
        self.assertIn(b"test wiki post", response.data)

    def test_wiki_edit(self):
        response = self.client.post("/login", data=dict(username="Admin", password="password", ip="127.0.0.1"), follow_redirects=True)
        response = self.client.get("/_edit/testpage/", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"testpage", response.data)
        self.assertIn(b"test wiki post", response.data)
        response1 = self.client.post("/_edit/testpage/", data=dict(content="this is an edit"), follow_redirects=True)
        self.assertEqual(response1.status_code, 200)
        self.assertIn(b"You just edited wiki page <u>testpage</u>", response1.data)
        self.assertIn(b"this is an edit", response1.data)
        self.assertIn(b"<p><strong>Version:</strong> 2</p>", response1.data)

    def test_wiki_history(self):
        response = self.client.get("/testpage/_history",content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"testpage", response.data)
        self.assertIn(b"test wiki post", response.data)

    def test_create_wiki(self):
        response = self.client.post("/login", data=dict(username="Admin", password="password", ip="127.0.0.1"), follow_redirects=True)
        response = self.client.get("/newpage", follow_redirects=True)
        response1 = self.client.get("/_new/newpage", content_type="html/text")
        self.assertEqual(response1.status_code, 200)
        self.assertIn(b"create a new wiki page named <i>newpage</i>", response1.data)
        response2 = self.client.post("/_new/newpage", data=dict(content="new post", page_name="newpage", version=1, user_id=1), follow_redirects=True)
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b"You just created a new wiki named <u>newpage</u>", response2.data)

