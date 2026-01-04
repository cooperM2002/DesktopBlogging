import json
from blogging.blog import Blog

class BlogDecoder(json.JSONDecoder):

    """
    blog object json encoder
    reconverts to blog from

    uses the object hook s.t when json loads, it sees a dict that looks similar to a blog
    then turns it into a blog instance
    """

    ####initiliaze, inject object hook
    def __init__(self,*args,**kwargs):

        #pass object hook to json decoder
        super().__init__(
            object_hook=self.object_hook,
            *args,
            **kwargs
        )

    ####converts dicts to blog instance
    def object_hook(self, o):

        #blog expected to have these four keys
        if(
            isinstance(o,dict)
            and "id" in o
            and "name" in o
            and "url" in o
            and "email" in o
        ):
            #rebuild blog object from dict
            return Blog(
                o["id"],
                o["name"],
                o["url"],
                o["email"]
            )
        
        #if not a blog => return unchanged
        return o
        