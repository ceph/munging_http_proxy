#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='munging_http_proxy',
    version='0.0.1',
    packages=find_packages(),

    author='Tommi Virtanen',
    author_email='tommi.virtanen@dreamhost.com',
    description='Munging HTTP proxy, for developing and debugging',
    license='MIT',
    keywords='web http testing',

    install_requires=[
        'gevent ==0.13.6',
        'webob',
        'wsgiproxy',
        ],

    entry_points={
        'console_scripts': [
            'interactive-http-proxy = munging_http_proxy.interactive:main',
            ],
        },

    )
