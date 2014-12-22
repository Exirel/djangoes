"""djangoes

A way to integrate ElasticSearch into a Django project.

No, this is not an ElasticSearch based ORM.
"""

from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Plugins',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name="djangoes",
    version="0.1.0",
    packages=find_packages(exclude=('tests',)),

    install_requires=[
        'django>=1.7',
        'elasticsearch>=1.2'
    ],

    # metadata for upload to PyPI
    author="Florian Strzelecki",
    author_email="florian.strzelecki@gmail.com",
    description="A way to integrate ElasticSearch into a Django project. "
                "No, this is not an ElasticSearch based ORM.",
    license="CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    keywords="django elasticsearch pytest",
    url="https://github.com/exirel/djangoes/",   # project home page, if any

    # Misc
    classifiers=classifiers,

    # Entry point
    entry_points = {
        'pytest11': [
            'djangoes = djangoes.test.pytest',
        ]
    },

)
