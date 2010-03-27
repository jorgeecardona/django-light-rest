from django.http import HttpResponse
from django.utils import simplejson
from django.db.models.query import QuerySet
from django.db.models import Model
from django.db.models.base import ModelBase

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

def retrieve(fields = None, add_to_dict = None, timestamp = None, collection = None):
    def dec(f):
        def new_f(request, *args, **kwords):

            # Call the function, it suppose to return a QueryDict
            result = f(request, *args, **kwords)
            
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
            return HttpResponse(result_string)

        return new_f
    return dec

def list(fields = None, add_to_dict = None, timestamp = None, collection = None):
    def dec(f):
        def new_f(request, *args, **kwords):

            if request.method == 'GET':
                
                # Call the function, it suppose to return a QuerySet or a list, 
                result = f(request, *args, **kwords)
                
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
                return HttpResponse(result_string)
            else:
                raise IncorrectMethod("Incorrect retrieve methd, use only GET.")

        return new_f
    return dec

from django.forms import Form

def create(form = None, collection=None, create_method=None, fields = None, add_to_dict = None):
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
            return HttpResponse(result_string)
                    
        return new_f
    return dec


def delete(collection = None, get_entity = None):
    def dec(f):
        def new_f(request, *args, **kwords):

            if callable(get_entity):
                entity = get_entity(*args, **kwords)
                entity.delete()
                return HttpResponse(simplejson.dumps(True))

            result = f(request, *args, **kwords)
            if result:
                return HttpResponse(simplejson.dumps(True))
            return HttpResponse(simplejson.dumps(False))

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
