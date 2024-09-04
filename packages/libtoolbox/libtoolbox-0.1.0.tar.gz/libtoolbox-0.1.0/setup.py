# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libtoolbox']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libtoolbox',
    'version': '0.1.0',
    'description': 'A simple utility for creating directories.',
    'long_description': 'None',
    'author': 'Your Name',
    'author_email': 'your.email@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
