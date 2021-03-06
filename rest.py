from django.http import HttpResponse
from django.utils import simplejson
from django.db.models.query import QuerySet
from django.db.models import Model
from django.db.models.base import ModelBase

class Error(Exception):
    """
    Rest Error
    ==========

    This class is used to create a rest response with an error.
    """
    pass


class IncorrectMethod(Exception):
    pass

class IncorrectResult(Exception):
    pass

def from_entity_to_dict(entity, fields = None, add_to_dict = None):
    """
    This function pass a model entity to a dict, based on a list of fields
    and a callback function that compute extra (key,value) pairs.
    """
    
    if fields is None:
        first = entity.__dict__.items()
    else:
        first = [(field, getattr(entity, field)) for field in fields]
        
    if callable(add_to_dict):
        return dict(first + add_to_dict(entity).items())
    
    return dict(first)

def retrieve(fields = None, add_to_dict = None, timestamp = None, mimetype = "text/html", auth=None):
    def dec(f):
        def new_f(request, *args, **kwords):

            # Identify agent
#            agent = rbac.identfy_from_request(request)

            # Authenticate agent
#            if rbac.authenticate_agent():
#                pass

            # Authorize
            

            # Call the function, it suppose to return a QueryDict
            try:
                result = f(request, *args, **kwords)
            except Exception, e:
                # Create a response with an error code but with the error message.
                return HttpResponse(e, status=400)                
            
            # IF image return it as is.
            # TODO: Check a formal way to change actions in contextual way.
            if mimetype == "image/png":
                return HttpResponse(result, mimetype=mimetype)

            # Check for the result type
            if not isinstance(result, (Model, QuerySet)):
                raise IncorrectResult("Incorrect result returned by retrieve.")

            # Order by date 
            # TODO: why am i doing this??
            if type(result) is QuerySet and type(timestamp) is str:
                result = result.order_by(timestamp)
                
            # As this is a retrive select only the oldest
            if isinstance(result, QuerySet):
                result = result[0]
                    
            # Select the right fields
            result_list = from_entity_to_dict(result, fields, add_to_dict)
                
            # Serialize the object
            result_string = simplejson.dumps(result_list)

            # Return the string                
            return HttpResponse(result_string, mimetype = mimetype)

        return new_f
    return dec

def list(fields = None, add_to_dict = None, timestamp = None, collection = None, mimetype = "text/html"):
    def dec(f):
        def new_f(request, *args, **kwords):

            if request.method == 'GET':
                
                # Call the function, it suppose to return a QuerySet or a list, 
                try:
                    result = f(request, *args, **kwords)
                except Error, e:
                    # Create a response with an error code but with the error message.
                    return HttpResponse('')
                
                
                # Check for the result type
                if type(result) is not QuerySet:
                    raise IncorrectResult("Incorrect result returned by retrieve.")

                # Order by date
                if type(result) is QuerySet and type(timestamp) is str:
                    result = result.order_by(timestamp)
                                               
                # Select the right fields
                result_list = [from_entity_to_dict(entity, fields, add_to_dict) for entity in result]
                
                # Serialize the object
                result_string = simplejson.dumps(result_list)

                # Return the string
                return HttpResponse(result_string, mimetype = mimetype)
            else:
                raise IncorrectMethod("Incorrect retrieve methd, use only GET.")

        return new_f
    return dec

from django.forms import Form

def create(form = None, collection=None, create_method=None, fields = None, add_to_dict = None, mimetype = "text/html"):
    def dec(f):
        def new_f(request, *args, **kwords):

            if type(form) is not Form:
                pass

            if type(collection) is None:
                pass



            result = f(request, *args, **kwords)

            if result is None:
                res = HttpResponse('')
                res.status_code = 400
                return res
            
            # Check for the result type
            if not isinstance(result, (Model,)):
                raise IncorrectResult("Incorrect result returned by retrieve.")

            # Select the right fields
            result_list = from_entity_to_dict(result, fields, add_to_dict)
                
            # Serialize the object
            result_string = simplejson.dumps(result_list)

            # Return the string
            return HttpResponse(result_string, mimetype = mimetype)
                    
        return new_f
    return dec


def delete(collection = None):
    def dec(f):
        def new_f(request, *args, **kwords):

            try:
                result = f(request, *args, **kwords)
                result.delete()

            except Exception, e:
                # Create a response with an error code but with the error message.
                return HttpResponse(e, status=400)

            return HttpResponse('', status=204)

        return new_f
    return dec


def update(fields = None):
    def dec(f):
        def new_f(request, *args, **kwords):

            result = f(request, *args, **kwords)

            if result is None:
                res = HttpResponse('')
                res.status_code = 400
                return res
            
            # Check for the result type
            if not isinstance(result, (Model,)):
                raise IncorrectResult("Incorrect result returned by retrieve.")

            # Select the right fields
            result_list = from_entity_to_dict(result, fields, add_to_dict)
                
            # Serialize the object
            result_string = simplejson.dumps(result_list)

            # Return the string
            return HttpResponse(result_string)
        return new_f
    return dec
