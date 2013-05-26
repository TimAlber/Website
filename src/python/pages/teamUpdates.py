from django.template import Context,loader
from .. import posts
import AccessDenied, PageNotFound, logging
import urllib

def getPage(resource, user):
    split = str(resource).split('/')
    if(len(split) == 1):
        temp = loader.get_template("Updates.html")
        updates =  posts.getRecentPosts((user.permissions < 1))
        if(updates.count() > 0):
            cont = Context({"updates": updates, "user": user})
        else:
            cont = Context({"user": user})
        result = temp.render(cont)
        return result
    
    elif(split[1] == "New"):
        if(user.permissions >= 2):
            temp = loader.get_template("NewPost.html")
            cont = Context({"user": user})
            result = temp.render(cont)
            return result
        else:
            return AccessDenied.getPage(resource, user)
    

    elif(split[1] != "New"):
        
        if(len(split) == 2):
            temp = loader.get_template("Post.html")
            logging.info("single page post")
            try:
                title = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
                post = posts.getPost(title)
                if(user.permissions < 1 & post.restricted): return AccessDenied.getPage(resource, user)
                comments = posts.getComments(post)
                if(comments.count() == 0): comments = None
                cont = Context({"post": post, "comments": comments, "user": user})
                return temp.render(cont)
            except IndexError:
                return PageNotFound.getPage(resource)
            
        elif(split[2] == "Edit"):
            if(user.permissions < 2): return AccessDenied.getPage(resource, user)
            try:
                title = urllib.unquote(split[1].encode('ascii')).decode('utf-8')
                post = posts.getPost(title)
                temp = loader.get_template("editPost.html")
                cont = Context({"post": post, "user": user})
                return temp.render(cont)
            except IndexError:
                return PageNotFound.getPage(resource)
        