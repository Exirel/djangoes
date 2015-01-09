# djangoes

A way to integrate ElasticSearch into a Django project. No, this is not an
ElasticSearch based ORM.

## What is it?

* Provide a thread-safe connections handler to ElasticSearch that mimics how
  databases are configured in Django,
* Relies on the official ElasticSearch python client,
* Configure connections and indices separatly,
* Integration with django tests,
* Integration with py.test for django,

It wraps the
[python client for ElasticSearch](https://pypi.python.org/pypi/elasticsearch)
with a connections handler and gives an interface to configure and use it for
production and testing purpose.

[Read the documentation](http://djangoes.readthedocs.org/) online, and do not
hesitate to send feedback on github.

## Compatibilities

The current version of `djangoes` works only with Python 3.4 and ElasticSearch
server >= 1.3.

The versions of django used to test are Django 1.6 and Django 1.7. The version
of elasticsearch-py used is 1.3.0.

There is no plan to support an older version of Python, Django, or
ElasticSearch.

## Install

You must use `pip` to install the latest version of `djangoes` and its
dependencies:

    pip install django elasticsearch djangoes

If you are not using a virtualenv, you may need to use `pip3` and not `pip` -
it depends on your Linux distribution and configuration.

## License

CC0, or Public Domain when it is possible and equivalent (it's kind of
complicated for some countries). If you are not sure: CC0.

## Contribute

Djangoes is distributed under the CC0 license, so anyone can contribute:
issues, PR, ideas, proposals, congrats, and tests.

If you want to submit a PR, You need to provide:

* PEP8 complient source code with docstring,
* documentation (in docs),
* unit-tests.

I'm working on making automated tests on the code that perform requests to
ElasticSearch, so the current situation is not perfect yet.

### Development environement

So, if you want to contribute, you need to install a development environement.

You will need to install ElasticSearch and a virtualenv. As a Ubuntu user, I
install ElasticSearch using the
[provided repository](http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/setup-repositories.html).

Then I use virtualenv wrapper to create my environment and git to clone the
github repository:

    mkproject djangoes --python=python3
    cd djangoes
    git clone git@github.com:exirel/djangoes

Then, you must use pip to install dependencies:

    pip install -r requirements.txt

Then you can run tests and get coverage and pylint report

    make test
    make report

Or, if you are lazy like me:

    make all

You can build the doc too:

    make doc

