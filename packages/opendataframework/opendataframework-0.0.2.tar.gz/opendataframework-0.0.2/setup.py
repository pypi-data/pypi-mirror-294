# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['opendataframework',
 'opendataframework.api',
 'opendataframework.api.api-postgres.app']

package_data = \
{'': ['*'],
 'opendataframework': ['analytics/*',
                       'analytics/superset/*',
                       'analytics/superset/database/postgres/*',
                       'devcontainers/R/.devcontainer/*',
                       'devcontainers/python/.devcontainer/*',
                       'layouts/research/.vscode/*',
                       'layouts/research/code/build/*',
                       'layouts/research/code/check/*',
                       'layouts/research/code/learn/*',
                       'layouts/research/code/share/*',
                       'layouts/research/data/derived/*',
                       'layouts/research/data/raw/*',
                       'layouts/research/libraries/*',
                       'layouts/research/logs/*',
                       'layouts/research/models/*',
                       'layouts/research/output/figures/*',
                       'layouts/research/output/tables/*',
                       'layouts/research/paper/*',
                       'storage/*',
                       'storage/postgres/*',
                       'utility/*',
                       'utility/texlive/*',
                       'utility/texlive/mnt/*'],
 'opendataframework.api': ['api-postgres/*']}

install_requires = \
['typer>=0.12.3,<0.13.0']

entry_points = \
{'console_scripts': ['opendataframework = opendataframework.__main__:main']}

setup_kwargs = {
    'name': 'opendataframework',
    'version': '0.0.2',
    'description': 'Open Data Framework is an open source, full stack data framework.',
    'long_description': '# Open Data Framework\nOpen source, full stack data framework.\n',
    'author': 'mykytapavlov',
    'author_email': 'mykytapavlov@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/opendataframework/opendataframework',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
