# djangoes

Integrates ElasticSearch and Django. Not an ElasticSearch based ORM.

## Features

``djangoes`` wraps the
[Python client for ElasticSearch](https://pypi.python.org/pypi/elasticsearch)
with a connections handler and gives an interface to configure and use it for
production and testing purpose.

* Thread-safe connection handler that mimics Django's ``DATABASES`` handling
* Uses official ElasticSearch Python client.
* Connections and indices can be configured separately.
* Integration with Django's native tests and py.test

Please [read the documentation](http://djangoes.readthedocs.org/), and do not
hesitate to send feedback on GitHub.

## Compatibility

The current version of `djangoes` works only with Python 3.4 and ElasticSearch
server >= 1.3.

Django 1.6 and 1.7 are tested, and elasticsearch-py 1.3.0 is used.

There are no plans to support older versions of Python, Django, or
ElasticSearch.

## Install

Use `pip` to install the latest version of `djangoes` and its
dependencies:

    $ pip install django elasticsearch djangoes

If you are not using a virtualenv, you may need to use `pip3` and not `pip` -
it depends on your Linux distribution and configuration.

## License

CC0, or Public Domain when it is possible and equivalent (it's kind of
complicated for some countries). If you are not sure: CC0.

## Contribute

`djangoes` is distributed under the CC0 license, so anyone can contribute:
issues, PR, ideas, proposals, congrats, and tests.

If you want to submit a PR, please also think of the following:

* PEP8 compliant source code with docstrings,
* documentation,
* unit tests.

I'm working on making automated tests on the code that perform requests to
ElasticSearch, so the current situation is not perfect yet.

### Development environment

If you'd like to contribute, you will need to install ElasticSearch and create 
a virtualenv. In Ubuntu, you can
install ElasticSearch using the
[provided repository](http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/setup-repositories.html).

Then you can use `virtualenvwrapper` to create the virtualenv and `git` to clone the
GitHub repository:

    $ mkproject --python=/usr/bin/python3.4 djangoes
    $ cd djangoes
    $ git clone git@github.com:exirel/djangoes .

Use pip to install dependencies:

    $ pip install -r requirements.txt

Then you can run the tests:

    $ make test
  
Or compile a coverage and pylint report:

    $ make report

Or, if you are lazy like me:

    $ make all

You can build the doc too:

    $ make doc
    $ xdg-open docs/_build/html/index.html
