[![Build Status](https://travis-ci.org/rzanluchi/keyard.svg?branch=dev)](https://travis-ci.org/rzanluchi/keyard)
# Keyard #

This project is a implementation of a Service Registry to work with the service discovery system.


# Getting started #

Aswe are not on pypi you need to clone this repo to use it

```
git clone git@github.com:rzanluchi/keyard.git
cd keyard
pip install .
```

Probably you want to use a virtualenv

# Configuring #

Keyard uses a json file configuration where you can set and etcd connection or use a in memory store

```
{
    "store_type": "etcd",
    "etcd": {
        "host": "localhost",
        "base_path": "/services"
    }
}
```
store_type can be 'etcd' or 'simple'

And to load the config create a python file like this bellow

```
from keyard import app
from keyard.helpers import config

config.load_file('example/config.json')
app = app.create_app()
``` 

the create_app prepares all keyard resources and routes


# Running #

You will need some WSGI server like gunicorn

```
gunicorn your_file:app -b 0.0.0.0:8000

```

# How to use it? #

Now you have a service running at port 8000 and you have a resource on <host>:8000/keyard where you can perform all the valid operations

## GET ##
A get will return the list of the services available based on the query string parameters 
* service_name -> name of the service you want (required)
* version -> version of the service you want (not required)
* load_balancer_strategy -> defines the load balancer strategy on server (not required)(only have 'random' for now)

Not using version will return all matches for the service_name for all version.
Not using load_balancer_strategy will return a list of all location available, using random the server chooses one and return it

## POST ##
A post will register a service on keyard. In the data you need service_name, version and a location. Version is not required and when not passe keyard assumes 1.0

## PUT ##
This method is intended for health_check calls. Health check calls are made to inform keyard that a location is still up. 

It uses the same data as post.

## DELETE ##
A delete will remove a location from keyard. Uses the same data as post



# License #

The MIT License (MIT)

Copyright (c) 2015, Raphael Bernardi Zanluchi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
