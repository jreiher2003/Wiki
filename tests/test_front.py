import unittest 
from base import BaseTestCase 

class TestAdoptorCase(BaseTestCase):

    def test_index_front(self):
        response = self.client.get('/',content_type='html/text')
        self.assertEqual(response.status_code, 200)