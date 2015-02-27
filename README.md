# [Flask-Config](https://github.com/salsita/flask-config) <a href='https://github.com/salsita'><img align='right' title='Salsita' src='https://www.google.com/a/cpanel/salsitasoft.com/images/logo.gif?alpha=1' /></a>

Flask configuration class.

[![Latest Version](https://pypip.in/version/Flask-Config/badge.svg)]
(https://pypi.python.org/pypi/Flask-Config/)
[![Downloads](https://pypip.in/download/Flask-Config/badge.svg)]
(https://pypi.python.org/pypi/Flask-Config/)
[![Supported Python versions](https://pypip.in/py_versions/Flask-Config/badge.svg)]
(https://pypi.python.org/pypi/Flask-Config/)
[![License](https://pypip.in/license/Flask-Config/badge.svg)]
(https://pypi.python.org/pypi/Flask-Config/)


## Supported Platforms

* [Python](http://www.python.org/) >= 2.6, 3.3
* [Flask](http://flask.pocoo.org/) >= 0.9


## Get Started

Install using [pip](https://pip.pypa.io/) or [easy_install](http://pythonhosted.org/setuptools/easy_install.html):
```bash
pip install Flask-Config
easy_install Flask-Config
```

## Example:

#### Flask application: `app.py`

```python
#!/usr/bin/env python

"""Flask-based web application."""

__all__ = 'app'.split()

import flask
from config import Config

app = flask.Flask(__name__)
app.config.from_object(Config)

if __name__ == '__main__':
    app.run()
```

#### Flask configuration: `config.py`

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Flask configuration for different environments."""

from __future__ import print_function

__all__ = '''
    Config
    ProductionConfig
    StagingConfig
    ExperimentalConfig
    TestingConfig
    DevelopmentConfig
    '''.split()

import flask.ext.config

Config = flask.ext.config.createConfig(__name__,
    updateEnvDefaults = dict(
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://dev:dev@localhost:3306/my_db'
    ))

# Configuration for different environments
class ProductionConfig(Config):
    """Configuration for production."""
    ENV_ID = 'prod'
    DEBUG = False

class StagingConfig(Config):
    """Configuration for staging
    """
    ENV_ID = 'stage'
    DEVELOPMENT = True
    DEBUG = True

class ExperimentalConfig(Config):
    """Configuration for experimental staging."""
    ENV_ID = 'try'
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    """Configuration for testing."""
    ENV_ID = 'qa'
    TESTING = True

class DevelopmentConfig(Config):
    """Configuration for development."""
    ENV_ID = 'dev'
    DEVELOPMENT = True
    DEBUG = True

# Aliases for different environment configurations
ProdConfig = ProductionConfig
StageConfig = StagingConfig
TryConfig = ExperimentalConfig
QaConfig = TestingConfig
TestConfig = TestingConfig
DevConfig = DevelopmentConfig

# Initialize requested config
Config.select()


# Print current configuration when run from command line
if __name__ == '__main__':
    print(Config)
```


## Changelog

### 0.1.1

#### Fixes

- Fix package setup to not require dependencies preinstalled.

### 0.1.0

#### Features

* Initial release.
