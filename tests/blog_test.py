from unittest import TestCase
from blogging.blog import Blog

class BlogTest(TestCase):


    def setUp(self):

        self.blog = Blog(1111110000, "test", "test_url", "test@example.com")


    def test_add_post_and_get_post(self):

        p1 = self.blog.add_post("first", "body1")
        p2 = self.blog.add_post("second", "body2")

        self.assertEqual(1, p1.code)
        self.assertEqual(2, p2.code)
        self.assertIs(self.blog.get_post(p1.code), p1)
        self.assertIsNone(self.blog.get_post(999))


    def test_update_info_blog(self):

        self.blog.update_info_blog(name="new", url="new_url", email="new@example.com")
        self.assertEqual("new", self.blog.name)
        self.assertEqual("new_url", self.blog.url)
        self.assertEqual("new@example.com", self.blog.email)


    def test_find_posts_matches_title_text_author(self):

        self.blog.add_post("thinking", "x", "hello")
        self.blog.add_post("other", "i think so", "bob")
        self.blog.add_post("No match", "zzz", "zzz")
 
        result = self.blog.find_posts("think")
        titles = [p.title for p in result]

        self.assertIn("thinking", titles)
        self.assertIn("other", titles)
        self.assertNotIn("no match", titles)


    def test_update_info_post(self):

        p = self.blog.add_post("old", "old body", "old author")
        ok = self.blog.update_info_post(p.code, "new", "new body", "new author")

        self.assertTrue(ok)

        updated = self.blog.get_post(p.code)

        self.assertEqual("new", updated.title)
        self.assertEqual("new body", updated.text)
        self.assertEqual("new author", updated.author)

        self.assertFalse(self.blog.update_info_post(999, "X"))


    def test_delete_post_by_code(self):

        p1 = self.blog.add_post("first", "B1")
        p2 = self.blog.add_post("second", "B2")

        self.assertTrue(self.blog.delete_post_by_code(p1.code))
        self.assertIsNone(self.blog.get_post(p1.code))
        self.assertIsNotNone(self.blog.get_post(p2.code))

        self.assertFalse(self.blog.delete_post_by_code(p1.code))


    def test_posts_listed_descending(self):

        p1 = self.blog.add_post("first", "B1")
        p2 = self.blog.add_post("second", "B2")
        p3 = self.blog.add_post("third", "B3")

        ordered = self.blog.posts_listed_descending()
        codes = [p.code for p in ordered]
        self.assertEqual([p3.code, p2.code, p1.code], codes)