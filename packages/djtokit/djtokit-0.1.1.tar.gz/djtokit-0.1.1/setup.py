# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djtokit',
 'djtokit.ctx',
 'djtokit.custom_db',
 'djtokit.custom_db.mysql',
 'djtokit.custom_db.router',
 'djtokit.dbusing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'djtokit',
    'version': '0.1.1',
    'description': 'A simple utility for creating directories.',
    'long_description': 'None',
    'author': 'pytools',
    'author_email': 'hyhlinux@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
