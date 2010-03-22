from django.http import HttpResponse

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


