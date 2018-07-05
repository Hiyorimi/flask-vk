#!/usr/bin/env python
"""
    flask_vk
    ~~~~~~~~~~~~~~~~

    Python vk module as a flask extension

    :copyright: (c) 2018 by Kirill Malev.
    :license: WTFPL, see LICENSE for more details.
"""
from setuptools import setup


setup(
    name='Flask-VK',
    version='1.0',
    url='https://github.com/Hiyorimi/flask-vk',
    license='BSD',
    author='Kirill Malev',
    author_email='kirill@malev.ru',
    description='VK API module support for your Flask application',
    long_description=__doc__,
    py_modules=['flask_vk'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.10',
        'vk>=2.0.2'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
