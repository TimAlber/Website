from django.template import Context,loader

def getPage(resource, user):
        temp = loader.get_template("about.html")
        cont = Context({})
        result = temp.render(cont)
        return result