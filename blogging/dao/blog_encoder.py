import json
from blogging.blog import Blog

class BlogEncoder(json.JSONEncoder):

    """
    blog object json encoder
    converts blog instance into dict
    """


    ####override default method to handle blog objects
    def default(self, o):

        #if this is a blog instance => convert to dict
        if isinstance(o, Blog):

            return{
                "id":o.id,      #blog id
                "name":o.name,  #blog name
                "url":o.url,    #blog url
                "email":o.email,#blog contact email
            }

        #fallback to default
        return super().default(o)