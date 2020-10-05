#!/usr/bin/env python
# flake8: noqa
import os
import sys
import bluebottle
from setuptools import setup, find_packages


def read_file(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()


readme = read_file('README.rst')
changes = ''

install_requires = [
    'Babel',
    'Django',
    'Pillow',
    'beautifulsoup4',
    'bleach',
    'clamd',
    'celery<5',
    'dotted',
    'defusedxml',
    'django-admin-sortable',
    'django-admin-tools',
    'django-adminfilters',
    'django-appconf',
    'django-axes',
    'django-choices',
    'django-cors-headers',
    'django-daterange-filter',
    'django-dynamic-fixture',
    'django-elasticsearch-dsl',
    'django-extensions',
    'django-filter',
    'django-fluent-dashboard',
    'django-fsm',
    'django-hashers-passlib',
    'django-ipware',
    'django-jet',
    'django-localflavor',
    'django-lockdown',
    'django-loginas',
    'django-map-widgets',
    'django-memoize',
    'django-modeltranslation',
    'django-money',
    'django-nested-inline',
    'django-parler<2.2',
    'django-permissions-widget',
    'django_polymorphic',
    'django-recaptcha',
    'django-rest-polymorphic',
    'django-rest-swagger',
    'django-singleton-admin',
    'django-subquery',
    'django-summernote',
    'django-taggit',
    'django-tinymce',
    'django-tools',
    'django-uuidfield',
    'django-wysiwyg',
    'djangorestframework-jsonapi',
    'drf-jwt',
    'djangorestframework',
    'dkimpy',
    'elasticsearch',
    'elasticsearch-dsl',
    'geocoder',
    'gunicorn',
    'html5lib',
    'icalendar',
    'influxdb',
    'lipisha',
    'lxml',
    'micawber',
    'mixpanel',
    'munch',
    'django-multiselectfield',
    'openpyxl',
    'pendulum',
    'psycopg2-binary',
    'pyasn1',
    'pygeoip',
    'pyjwt',
    'python-dateutil',
    'python-magic',
    'python-memcached',
    'python3-saml==1.9.0' if sys.version_info.major == 3 else 'python-saml==2.1.7',
    'python-social-auth',
    'social-auth-app-django',
    'surlex',
    'rave-python',
    'raven',
    'regex',
    'requests',
    'schwifty',
    'sorl-thumbnail',
    # 'sorl-thumbnail @ git+https://github.com/mariocesar/sorl-thumbnail.git@v12.3#egg=sorl-thumbnail-12.3-github',
    'South',
    'Sphinx',
    'staticmaps-signature',
    'stripe',
    'suds-jurko',
    'SurveyGizmo',
    'tablib',
    'timezonefinder',
    'unicodecsv',
    'wheel',
    'xlsxwriter',

    # Github requirements
    'django-exportdb @ git+https://github.com/onepercentclub/django-exportdb.git@0.4.8#egg=django-exportdb-0.4.8-github',
    'django-tenant-schemas @ git+https://github.com/jayvdb/django-tenant-schemas.git@migrate-fix#egg=django-tenant-schemas-1.10.0',
    'django-tenant-extras @ git+https://github.com/jayvdb/django-tenant-extras.git@dj3-template-loader#egg=django-tenant-extras-2.0.14',
    'django-taggit-autocomplete-modified @ git+https://github.com/onepercentclub/django-taggit-autocomplete-modified.git@8e7fbc2deae2f1fbb31b574bc8819d9ae7c644d6#egg=django-taggit-autocomplete-modified-0.1.1b1',
    'django-fluent-contents @ git+https://github.com/jayvdb/django-fluent-contents.git@issue-106#egg=django-fluent-contents-2.0.7',
    'django-geoposition @ git+https://github.com/bedubs/django-geoposition#egg=django-geoposition-0.3.0',
]

tests_requires = [
    'coverage',
    'coveralls',
    'django-nose',
    'django-setuptest',
    'django-slowtests',
    'django-webtest',
    'factory-boy',
    'httmock',
    'mock==4.0.2' if sys.version_info.major == 3 else 'mock==3.0.5',
    'nose',
    'pylint',
    'pyquery',
    'pylint-django',
    'tblib',
    'tdaemon',
    'WebTest',
    'sniffer',
    'vine'
]

dev_requires = [
    'ipdb',
    'flake8'
]

setup(
    name='bluebottle',
    version=bluebottle.__version__,
    license='BSD',

    # Packaging.
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=install_requires,

    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': dev_requires,
        'test': tests_requires,
    },
    include_package_data=True,
    zip_safe=False,

    # Metadata for PyPI.
    description='Bluebottle, the crowdsourcing framework initiated by the 1%Club.',
    long_description='\n\n'.join([readme, changes]),
    author='1%Club',
    author_email='info@onepercentclub.com',
    platforms=['any'],
    url='https://github.com/onepercentclub/bluebottle',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ]
)
