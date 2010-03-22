# Django light rest

This project is a collection of few files in order to ease the definition of a rest interface in django.

## urls.py

Basically one can't define a handler of an url based on the http method directly in the urls files. This separation is needed for a rest interface in order to separate responsabilities on actions.
A good way to add this separation is to always use a central rest dispatcher like this:

`
url(r'^rest/users/?$', 'core.rest.dispatcher', {
    'GET'  : 'core.rest.users.list',
    'POST' : 'core.rest.users.create',
    }),

url(r'^rest/users/(?P<user_id>[^/]+)/?$', 'core.rest.dispatcher', {
    'GET': 'core.rest.users.retrieve'
    }),

`

## rest dispatcher