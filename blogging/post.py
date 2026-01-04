from datetime import datetime

class Post:
    def __init__(self, code, title, text, author=None):
        self.code = code
        self.title = title
        self.text = text
        self.author = author
        self.created_at = datetime.now()
        self.updated_at = self.created_at


    #Update the timestamp for when the post was last modified
    def update_time(self):
        self.updated_at =datetime.now()#lil fix


    #for tests
    def __eq__(self, other):
        return(
            #Compare posts by code, title, and text.
            isinstance(other,Post)#fixedtypo
            and self.code==other.code
            and self.title==other.title
            and self.text==other.text
        )


    def __repr__(self):
        return f"Post(code={self.code}, title={self.title!r})"


    def __str__(self):
        return f"[{self.code}] {self.title}"