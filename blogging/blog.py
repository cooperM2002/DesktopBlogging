from blogging.dao.post_dao_pickle import PostDAOPickle
from .post import Post
from blogging.configuration import Configuration

class Blog:
    def __init__(self, id, name, url, email):
        self.id = id
        self.name = name
        self.url = url
        self.email = email


        self.next_post_id = 1

        #initialize dao with autosave from config
        config = Configuration()
        autosave = config.__class__.autosave
        self.post_dao = PostDAOPickle(self, autosave=autosave)



    #for tests
    #compare id, name, url, email
    def __eq__(self, other):
        
        return(
            isinstance(other,Blog)
            and self.id==other.id
            and self.name==other.name
            and self.url==other.url
            and self.email==other.email
        )

    ########################
    ## (3 to 9) blog ops  ##
    ########################


    ####(6)helper for updating blog info
    def update_info_blog(self, name=None, url=None, email=None):

        #name exists
        if name is not None: self.name=name
        #url exists
        if url is not None: self.url=url #fixed name to url
        #email exists
        if email is not None: self.email=email #fixed name to email


    ##########################
    ## (10 to 14) post ops  ##
    ##########################

    ####for (10) create_post
    #create new post,increment code,sets timestamps
    def add_post(self, title, text, author=None):

        code=self.next_post_id

        post=Post(code, title, text, author)

        self.post_dao.create_post(post)

        #increment for next added
        self.next_post_id+=1

        return post



    #####for some controller post methods
    def get_post(self, code):

        return self.post_dao.search_post(code)


    
    ####(11)retrieve posts query title,text, not case sensitive
    def find_posts(self, query):

        return self.post_dao.retrieve_posts(query)
        


    #####(12)update existing post by code, updates timestamp
    #####helper for updating post info
    def update_info_post(self, code, title=None, text=None, author=None):
        
        #use dao to update title,text
        updated = self.post_dao.update_post(code, title, text)
        if not updated: return False


        post = self.get_post(code)

        #check existence
        if post is None: return False

        #author exists
        if author is not None:

            post.author=author
            post.update_time()

        
        #make sure change is persistent
        if getattr(self.post_dao, "autosave", False):
            self.post_dao.save_to_file()

        return True



    #####(13)delete post by code
    def delete_post_by_code(self, code):

        return self.post_dao.delete_post(code)



    ####(14)list all posts newest to oldest
    def posts_listed_descending(self):
        # from newest to oldest (higher code first).
        return self.post_dao.list_posts()
