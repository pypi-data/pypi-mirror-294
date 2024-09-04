# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chatsky_ui',
 'chatsky_ui.api',
 'chatsky_ui.api.api_v1',
 'chatsky_ui.api.api_v1.endpoints',
 'chatsky_ui.clients',
 'chatsky_ui.core',
 'chatsky_ui.db',
 'chatsky_ui.db.crud',
 'chatsky_ui.db.models',
 'chatsky_ui.schemas',
 'chatsky_ui.services',
 'chatsky_ui.tests',
 'chatsky_ui.tests.api',
 'chatsky_ui.tests.e2e',
 'chatsky_ui.tests.integration',
 'chatsky_ui.tests.services',
 'chatsky_ui.utils']

package_data = \
{'': ['*'], 'chatsky_ui': ['static/*']}

install_requires = \
['aiofiles>=23.2.1,<24.0.0',
 'cookiecutter>=2.6.0,<3.0.0',
 'dff==0.6.4.dev0',
 'fastapi>=0.110.0,<0.111.0',
 'httpx-ws>=0.6.0,<0.7.0',
 'httpx>=0.27.0,<0.28.0',
 'omegaconf>=2.3.0,<3.0.0',
 'pydantic-settings>=2.2.1,<3.0.0',
 'pydantic>=2.6.3,<3.0.0',
 'pylint>=3.2.3,<4.0.0',
 'pytest-asyncio>=0.23.6,<0.24.0',
 'pytest-mock>=3.14.0,<4.0.0',
 'pytest>=8.1.1,<9.0.0',
 'sphinx',
 'sphinx-rtd-theme',
 'typer>=0.9.0,<0.10.0',
 'uvicorn[standard]>=0.28.0,<0.29.0']

entry_points = \
{'console_scripts': ['chatsky.ui = chatsky_ui.cli:cli']}

setup_kwargs = {
    'name': 'chatsky-ui',
    'version': '0.2.0',
    'description': 'Chatsky-UI is GUI for Chatsky Framework, that is a free and open-source software stack for creating chatbots, released under the terms of Apache License 2.0.',
    'long_description': '',
    'author': 'Denis Kuznetsov',
    'author_email': 'kuznetsov.den.p@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
