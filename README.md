# Django light REST

This project is a collection of files that ease the definition of a rest interface in django.

## urls.py

Basically one can't define a handler of an url based on the http method directly in the urls files. A single handler for an url has to be defined, and inside one add code to check the http method. 

This separation is needed for a rest interface in order to separate responsabilities on actions.

A good way to add this separation is to always use a central rest dispatcher with a new funcion like this:

    url_rest(r'^users/?$',  
             get = 'core.rest.user.list',
             post = 'core.rest.user.create'
             ),

    url_rest(r'^users/(?P<user_id>[^/]+)/?$',  
             get = 'core.rest.user.retrieve',
             put = 'core.rest.user.update',
	     delete = 'core.rest.user.delete',
             ),

We can now define a different handler for each method in a single url without add code to the handlers itself, the `core.rest.dispatcher` does the trick.

A good point here is that we don't import code in urls so its load process will be lighter.

## REST dispatcher

It just receive the request and the method 

