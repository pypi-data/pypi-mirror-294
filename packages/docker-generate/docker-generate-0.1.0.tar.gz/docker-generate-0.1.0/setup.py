# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['docker_generate']
install_requires = \
['anthropic>=0.34.2,<0.35.0',
 'click-spinner>=0.1.10,<0.2.0',
 'click>=8.1.7,<9.0.0',
 'openai>=1.43.0,<2.0.0',
 'prompt-toolkit>=3.0.47,<4.0.0',
 'pydantic>=2.8.2,<3.0.0']

entry_points = \
{'console_scripts': ['docker-gen = src.docker_gen:main']}

setup_kwargs = {
    'name': 'docker-generate',
    'version': '0.1.0',
    'description': 'Generate Dockerfile(s) for your projects',
    'long_description': '# 🐋 Generate Dockerfile, on the fly\n\n```\n# Install\npip install docker-gen ploomber-cloud\n\n# Genetare a custom dockerfile four your project\ndocker-gen\n\n# Deploy your project\nploomber-cloud deploy\n```\n\n\n',
    'author': 'latentdream',
    'author_email': 'email@guillaume.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
