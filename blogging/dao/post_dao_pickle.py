import os
import pickle

from blogging.configuration import Configuration    #global config

from blogging.dao.post_dao import PostDAO           #implements


"""

    PostDAOPickle

    implements PostDao

    a data access object that stores posts and 
    depending on autosave on/off, persists them w/ pickle module

    autosave off: posts stored in self.posts
    autosave on: tries to load posts from file, any mutative method writes back to disk

"""

class PostDAOPickle(PostDAO):



############
##  init  ##
############

    def __init__(self, blog, autosave=False):

        self.autosave = autosave    #persist on/off
        self.blog = blog            #blog post is under
        self.posts = {}             #posts dict


        ####persistence

        config = Configuration()        #get config
        config_class = config.__class__ #class level config  

        self.records_path = config.__class__.records_path       #dict for post records
        self.records_extension = config_class.records_extension #file extension for record files
        os.makedirs(self.records_path, exist_ok=True)           #records dict exists
        
        #specific blog path
        self.filepath = os.path.join(
            self.records_path,
            f"{self.blog.id}{self.records_extension}"
        )

        #if autosave on => load existing posts from file
        if self.autosave: self.load_from_file()



#################
##   helpers   ##
#################



    ####load from json

    def load_from_file(self):

        #does not exist => nothing to load
        if not os.path.exists(self.filepath): return

        #read binary
        with open(self.filepath, "rb") as file:

            #try to load
            try: 
                loaded = pickle.load(file)

            #if empty or corrupted
            except Exception: 
                return

        #expect dict or list of posts
        if isinstance(loaded, dict): 
            self.posts = loaded
        
        else:
            temp = {}
            for post in loaded: 
                temp[post.code] = post

            self.posts = temp

        #update next id based on highest id value
        if self.posts:
            max_code  = max(self.posts.keys())
            self.blog.next_post_id = max_code +1

        #no posts on blog
        else:
            self.blog.next_post_id = 1



    ####writes to pickle file

    def save_to_file(self):

        #write bytes
        with open(self.filepath, "wb") as file:
            pickle.dump(self.posts, file)



##################
## main methods ##
##################



    ####find post by key

    def search_post(self, key):
        
        #post @ key
        post = self.posts.get(key)

        return post



    ####store new post to dao

    def create_post(self, post):
        
        #store by code
        self.posts[post.code]=post

        #autosave to file
        if self.autosave: self.save_to_file()

        return post



    ####get all posts w/ substring

    def retrieve_posts(self, search_string):
        
        #if empty or none
        if search_string is None or search_string == "":
            result = list(self.posts.values())
            return result

        #to lower
        query = search_string.lower()
        search_result = []

        #check post
        for post in self.posts.values():

            title_match = query in post.title.lower()   #check title
            text_match = query in post.text.lower()     #check text

            #only if author exists
            if post.author is not None:
                author_match = query in post.author.lower()

            else:
                author_match = False

            #if any field matches => keep
            if title_match or text_match or author_match:
                search_result.append(post)

        return search_result



    ####update title or text of post @ key

    def update_post(self, key, new_title, new_text):
        
        post=self.posts.get(key)

        #if no post @ key => do nothing
        if post is None: return False
        
        #title exists
        if new_title is not None: post.title=new_title

        #text exists
        if new_text is not None: post.text=new_text

        #update timestamp
        post.update_time()

        #autosave to file
        if self.autosave: self.save_to_file()

        return True
        

    
    ####delete post @ key

    def delete_post(self, key):
        
        #if code exists
        if key in self.posts:
            del self.posts[key]                     #delete post @ code
            if self.autosave: self.save_to_file()   #autosave to file

            return True
        
        return False



    ####list all posts in descending order

    def list_posts(self):


        posts=self.posts.values()

        ####simple helper
        def get_post_code(post): return post.code
        
        #sort posts in descending order
        posts_sorted = sorted(
            posts,
            key=get_post_code,
            reverse=True
            )
    
        return posts_sorted

            