import json
import os

from blogging.configuration import Configuration    #global config

from blogging.blog import Blog
from .blog_dao import BlogDAO                       #implements

from .blog_encoder import BlogEncoder
from .blog_decoder import BlogDecoder

"""

    BlogDAOJSON

    implements BlogDao

    a data access object that stores blog objects in a dictionary
    with the option of storing them on a json file when autosave is true

"""

class BlogDAOJSON(BlogDAO):



############
##  init  ##
############

    def __init__(self, autosave=False):

        self.autosave = autosave    #persist on/off
        self.blogs = {}             #blog dictionary
        config = Configuration()    #get config    

        self.blogs_file = config.__class__.blogs_file   #reads config from the class level
        if self.autosave: self.load_from_file()         #when autosave is on, try to load from disk



################
##   helpers  ##
################


    ####loads from json

    def load_from_file(self):

        #if json file doesn't exist, then there's nothing to load
        if not os.path.exists(self.blogs_file): return
        
        #open json file to read its contents
        with open(self.blogs_file,"r",encoding="utf-8") as file:

            #decode json file
            try:
                blogs_list=json.load(file, cls=BlogDecoder) #expect list of blog objects

            #if empty or corrupt
            except json.JSONDecodeError:
                return
            
        #blogs_list can be list of blog objs or dicts
        for item in blogs_list:

            #already a blog object
            if isinstance(item, Blog): 
                blog=item
            
            #or convert from dict
            else:
                blog = Blog(
                    item["id"],
                    item["name"],
                    item["url"],
                    item["email"],
                )

            #store back in the main dict
            self.blogs[blog.id] = blog


    ####writes to json

    def save_to_file(self):

        #convert dict to blog objects
        blogs_list = list(self.blogs.values())

        #open json to write
        with open(self.blogs_file, "w", encoding="utf-8") as file:
            json.dump(
                blogs_list, 
                file,
                cls=BlogEncoder,    #use blogencoder
                indent=2            #formatting
            )


###############
##  methods  ##
###############
    


    ####search by id

    def search_blog(self, key):

        blog = self.blogs.get(key)

        return blog



    ####add new blog to dao, with autosave on or off

    def create_blog(self, blog):

        #store by id
        self.blogs[blog.id]=blog
        
        #autosave to file
        if self.autosave: self.save_to_file()



    ###get all blogs containing search string

    def retrieve_blogs(self, search_string):
        
        #no search string => return all
        if search_string is None or search_string=="":

            result = list(self.blogs.values())
            return result

        #to lowercase
        search_string = search_string.lower()
        search_result = []

        #check eah name for substring
        for blog in self.blogs.values():

            name_lower = blog.name.lower()

            #if found ,keep that blog
            if search_string in name_lower:
                search_result.append(blog)

        return search_result



    ####replace blog @ key with current instance

    def update_blog(self, key, blog):

        #overwrite blog @ key
        self.blogs[key]=blog

        #autosave to file
        if self.autosave: self.save_to_file()



    ####delete blog @ key

    def delete_blog(self, key):
        
        #replace blog @ key if key exists
        if key in self.blogs:

            #remove from dict
            del self.blogs[key]

            #autosave to file
            if self.autosave: self.save_to_file()



    ####return a list of all objs that are stored

    def list_blogs(self):
        
        return list(self.blogs.values())


