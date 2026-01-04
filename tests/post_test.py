from unittest import TestCase
from blogging.post import Post
from time import sleep

class PostTest(TestCase):


    def test_init_sets_fields(self):

        p = Post(1, "title", "body", "author")

        self.assertEqual(1, p.code)
        self.assertEqual("title", p.title)
        self.assertEqual("body", p.text)
        self.assertEqual("author", p.author)
        self.assertIsNotNone(p.created_at)
        self.assertEqual(p.created_at, p.updated_at)


    def test_update_time_updates_updated_at(self):

        p = Post(1, "title", "body")
        
        old_created = p.created_at
        old_updated = p.updated_at

        sleep(0.001)
        p.update_time()

        #created_at not changed
        self.assertEqual(old_created, p.created_at)

        #updated_at should change
        self.assertNotEqual(old_updated, p.updated_at)