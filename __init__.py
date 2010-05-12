from django.http import HttpResponse

def url_rest(regexp, get = None, post = None, put = None, delete = None):

    methods = {}
    if get:
        methods['GET'] = get
        
    if post:
        methods['POST'] = post

    if put:
        methods['PUT'] = put

    if delete:
        methods['DELETE'] = delete

    return url(regexp, 'core.rest.dispatcher', delete)


def dispatcher(request, GET=None, POST=None, DELETE=None, PUT=None, **kwords):

    if request.method == 'GET' and type(GET) is str:

        # Get the base name and the internal module from the name
        name, internal = GET.rsplit(".",1)
        
        # Import the base bame
        module = __import__(name, fromlist=["*"])        
        
        # Get the internal module
        view = getattr(module, internal)

        if callable(view):
            return view(request, **kwords)        

    if request.method == 'POST' and  type(POST) is str:

        # Get the base name and the internal module from the name
        name, internal = POST.rsplit(".",1)
        
        # Import the base bame
        module = __import__(name, fromlist=["*"])        
        
        # Get the internal module
        view = getattr(module, internal)

        if callable(view):
            return view(request, **kwords)        

    if request.method == 'PUT' and  type(PUT) is str:

        request.method = 'POST'
        request._load_post_and_files()
        request.method = 'PUT'
        request.PUT = request.POST

        # Get the base name and the internal module from the name
        name, internal = PUT.rsplit(".",1)
        
        # Import the base bame
        module = __import__(name, fromlist=["*"])        
        
        # Get the internal module
        view = getattr(module, internal)

        if callable(view):
            return view(request, **kwords)        

    if request.method == 'DELETE' and  type(DELETE) is str:

        # Get the base name and the internal module from the name
        name, internal = DELETE.rsplit(".",1)
        
        # Import the base bame
        module = __import__(name, fromlist=["*"])        
        
        # Get the internal module
        view = getattr(module, internal)

        if callable(view):
            return view(request, **kwords)

    return HttpResponse("Error")


