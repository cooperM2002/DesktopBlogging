
import hashlib  #

from blogging.exception.illegal_access_exception import IllegalAccessException   #cant access
from blogging.exception.invalid_logout_exception import InvalidLogoutException   #bad logout
from blogging.exception.invalid_login_exception import InvalidLoginException     #bad login
from blogging.exception.duplicate_login_exception import DuplicateLoginException #no login when already logged in

from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException

from blogging.dao.blog_dao_json import BlogDAOJSON
from blogging.configuration import Configuration

from .blog import Blog


#--------------------------------------------------------------------------------------------
#
#   1. controller test:     python3 -m unittest -v tests.controller_test.ControllerTest
#
#   2. integration test:    python3 -m unittest -v tests.integration_test.IntegrationTest
#
#   3. blog test:           python3 -m unittest -v tests.blog_test.BlogTest
#
#   4. post test:           python3 -m unittest -v tests.post_test.PostTest                      
#
#---------------------------------------------------------------------------------------------






class Controller:

###############
##    init   ##
###############



    def __init__(self, autosave=False):

        ###setup fields

        config = Configuration()                    #config
        self.autosave = config.__class__.autosave   #autosave


        self.logged_in = None                               #default not logged in
        self.blog_dao = BlogDAOJSON(autosave=self.autosave) #when autosave true => save/load blog from json
        self.blogs = self.blog_dao.blogs                    #blog_dao methods
        self.current_blog_id = None                         #default no blog

        #old hardcoded users

        # self.users = {
        #     "user":  ("8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"),
        #     "ali":   ("6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810"),
        #     "kala":  ("e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e")
        # }


        ###setup users

        self.users = {}                             #users dict
        users_path = config.__class__.users_file    #user file

        try: 
            with open(users_path, "r", encoding="UTF-8") as file:
                
                for line in file:

                    line=line.strip()       #strip whitespace
                    if not line: continue   #skip empty

                    username, pw_hashed = line.split(",", 1)    #each line is (username,hashed password)
                    self.users[username] = pw_hashed            #mapping for login lookup

        except FileNotFoundError: self.users={} #fallback




##################
##    helpers   ##
##################

    #checking login in methods
    @property
    def is_logged_in(self):
        return self.logged_in is not None


    #hashes a password
    def hash_password(self, password):
        
        pw_bytes=password.encode("utf-8")       #string to bytes
        pw_hashed=hashlib.sha256(pw_bytes)      #hash the byte converted password
        pw_hashed_string=pw_hashed.hexdigest()  #turn hashed pw into 64 char string
        
        return pw_hashed_string



#############################
## (1,2) login and logout ##
############################



    ####(1) log in
    def login(self, username, password):

        #cant login again
        if self.is_logged_in: 
            raise DuplicateLoginException()

        #look up username, exit if username does not exist
        if username not in self.users:
            raise InvalidLoginException()

        #check password
        if self.users[username] != self.hash_password(password):
            raise InvalidLoginException()
        
        #log in
        self.logged_in=username
        
        return True



    ####(2) log out
    def logout(self):

        #not logged in -> cannot log out
        if not self.is_logged_in:
            raise InvalidLogoutException()

        #logout
        self.logged_in=None
        self.current_blog_id=None

        return True



##########################
## (3 to 8) blog ops    ##
##########################



    ####(4) create new blog

    def create_blog(self, blog_id, name, url, email):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()

        #if id already taken -> illegal operation
        if blog_id in self.blogs:
            raise IllegalOperationException("Blog ID already exists.")
            #return None

        #make new blog
        blog = Blog(blog_id,name,url,email)

        #add id
        self.blog_dao.create_blog(blog)

        return blog
        


    ####(3) search blog by id

    def search_blog(self, blog_id):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        
        searched = self.blog_dao.search_blog(blog_id)########

        return searched



    ####(8) list all blogs
    
    def list_blogs(self):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        
        return list(self.blogs.values())



    ####(5) retrieve blog by name substring

    def retrieve_blogs(self, name_substring):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        
        blogs_matched = self.blog_dao.retrieve_blogs(name_substring)

        return  blogs_matched



    ####(6) update existing blog

    def update_blog(self, old_id, new_id, name, url, email):

        #not logged in -> illegal access
        if not self.is_logged_in: raise IllegalAccessException()
        
        #cant update current blog -> illegal operation
        if self.current_blog_id == old_id: raise IllegalOperationException()
   
        # Retrieve the blog to update
        blog = self.blog_dao.search_blog(old_id)

        #blog must exist,if not -> illegal operation
        if blog is None: raise IllegalOperationException()
        
        dao_id=self.blog_dao.search_blog(new_id)

        #id conflict -> illegal operation
        if new_id != old_id and dao_id is not None: 
            raise IllegalOperationException()
        
        # Update blog information
        blog.update_info_blog(name=name, url=url, email=email)

        #tell dao that blog is updated
        if new_id == old_id:
            self.blog_dao.update_blog(old_id, blog)#couldnt update blogs
        
        else:

            self.blog_dao.delete_blog(old_id)   #remove
            blog.id=new_id                      #update id
            self.blog_dao.create_blog(blog)     #create w new id
            
            if  self.current_blog_id == old_id:
                self.current_blog_id = new_id   #if matched to old id, update it to new

        return True


    
    ####(7) delete existing blog

    def delete_blog(self, blog_id):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        

        #cannot delete blog that does not exist -> illegal operation
        if blog_id not in self.blogs:
            raise IllegalOperationException()
        
        #cannot delete active blog -> illegal operation
        if self.current_blog_id == blog_id:
            raise IllegalOperationException()
        
        # Perform deletion
        self.blog_dao.delete_blog(blog_id)

        return True
    


###########################
##   (9) current blog   ##
##########################

    # cannot do operation without logging in
    # cannot get current blog without setting it first
    # cannot set a non-existent blog to be the current blog
    # cannot delete the current blog, unset current blog first



    ####(9) choose or unset current blog

    def set_current_blog(self, blog_id):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        
        #check blog exists
        if blog_id not in self.blogs:
            raise IllegalOperationException() 
        
        #change current to the passed in id
        self.current_blog_id=blog_id



    ####(9.1)

    def get_current_blog(self):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()

        #if current is set to nothing
        if self.current_blog_id is None:
            return None
        
        #if current is set but not in list of blogs
        if self.current_blog_id not in self.blogs:
            return None
        
        #get blog at id
        blog = self.blog_dao.search_blog(self.current_blog_id)

        return blog

        
    ####(9.2)

    def unset_current_blog(self):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        
        self.current_blog_id=None

        return True



#######################
## (10 to 14) posts  ##
######################

    # cannot do operation without logging in
    # cannot do operation without a valid current blog



    ####(10)create post in current blog

    def create_post(self, title, text, author=None):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        
        #current blog
        blog = self.blog_dao.search_blog(self.current_blog_id)

        #valid blog
        if blog is None:
            raise NoCurrentBlogException()

        return blog.add_post(title, text, author)
        


    ####(10.1)search

    def search_post(self, code):
        
        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        
        #current blog
        blog = self.blog_dao.search_blog(self.current_blog_id)

        #valid blog
        if blog is None:
            raise NoCurrentBlogException()

        post_found = blog.get_post(code)

        return post_found
        


    ####(11)retrieve posts by text in current blog

    def retrieve_posts(self, query):
        
        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()

        #current blog
        blog = self.blog_dao.search_blog(self.current_blog_id)
        
        #valid blog
        if blog is None:
            raise NoCurrentBlogException()
        
        query_lower = query.lower()
        posts_matched = blog.find_posts(query_lower)

        return posts_matched

		 

    ####(12)update post in current blog

    def update_post(self, code, title=None, text=None, author=None):

        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        
        #current blog
        blog = self.blog_dao.search_blog(self.current_blog_id)

        #valid blog
        if blog is None:
            raise NoCurrentBlogException()
        
        post_updated=blog.update_info_post(code,title,text,author)

        #check code found in blog
        if not post_updated:
            return None

        return True



    # try to delete a post when there are no posts taken for that blog in the system
    # delete the remaining existing posts, regardless of deleting order

    ####(13)delete post in current blog

    def delete_post(self, code):
        
        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
           
        #current blog
        blog = self.blog_dao.search_blog(self.current_blog_id)

        #valid blog
        if blog is None:
            raise NoCurrentBlogException()

        # Attempt to delete, returns True/False
        post_deleted=blog.delete_post_by_code(code)

        return post_deleted
    
    

    ####(14)list posts in current blog from newest to oldest

    def list_posts(self):
        
        #not logged in -> illegal access
        if not self.is_logged_in:
            raise IllegalAccessException()
        
        blog = self.blog_dao.search_blog(self.current_blog_id)


        #valid blog
        if blog is None:
            raise NoCurrentBlogException()

        posts_sorted = blog.posts_listed_descending()
        
        return posts_sorted