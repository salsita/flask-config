"""Flask configuration class.

The configuration class is not expected to be instantiated. Create different configurations as its subclasses.
"""

__all__ = 'createConfig Config MetaConfig'.split()
__version__ = '0.1.0'

import os
import sys
import string

class MetaConfig(type):
    """Base configuration metaclass used to define class stringifier and read-only class properties.

    See https://stackoverflow.com/a/3203434/899047 on read-only class properties.
    """

    # Configurations namespace (default: class module)
    configurationsNamespace = None
    genericActiveConfigName = 'Config'

    def __init__(cls, name, bases, dct):
        cls.__str__ = MetaConfig.__str__.__get__(cls, cls.__class__)

        cls.ENV = cls.getEnvName(cls.__name__) or cls.ENV_ID

        if cls.envSelectProperty:
            setattr(cls, cls.envSelectProperty, cls.ENV)

        if not hasattr(cls, 'root'):
            cls.root = cls

        super(MetaConfig, cls).__init__(name, bases, dct)

    def __str__(cls):
        """Returns a string listing configuration keys and values."""
        return '\n'.join('{}: {!r}'.format(key, getattr(cls, key)) for key in dir(cls) if cls.isKey(key))

    @property
    def namespace(cls):
        """Read-only class property returning configurations namespace (e.g. module/class)."""
        return cls.configurationsNamespace or sys.modules[cls.__module__]

    @property
    def envSelectVar(cls):
        """Read-only class property returning environment select variable name."""
        return cls.envMap.get(cls.envSelectProperty, None)

    @property
    def configurations(cls):
        """Read-only class property returning list of available configuration classes."""
        configurations = set()

        for key in dir(cls.namespace):
            config = getattr(cls.namespace, key)

            if cls.isConfig(config):
                name = cls.getEnvName(key)

                if name:
                    if config in configurations:
                        config.names.add(name)
                    else:
                        configurations.add(config)
                        config.names = set([name])

        for config in configurations:
            config.names = sorted(config.names, key=len)
                # Sort config names by length, shortest first

        return sorted(configurations, key=lambda c: c.names[0])
            # Sort configurations alphabetically by their first name

class Config(object):
    """Base configuration class."""
    __metaclass__ = MetaConfig

    ENV_ID = 'base'
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True

    # Settings configurable with environment variables.
    env = os.environ
    envSelectProperty = 'ENV_SELECT'
    envMap = dict(
        ENV_SELECT = 'APP_ENV',
        SECRET_KEY = 'SECRET_KEY',
        SQLALCHEMY_DATABASE_URI = 'DATABASE_URL',
        )
    envHelp= dict(
        ENV_SELECT = 'select environment configuration',
        SECRET_KEY = 'secret key for signing session cookies',
        SQLALCHEMY_DATABASE_URI = 'sqlalchemy database uri including credentials',
        )
    envDefaults = dict(
        ENV_SELECT = 'dev',
        SECRET_KEY = 'This has to be changed on deployment using SECRET_KEY environment variable',
        )
    envInitialized = False
    envKeyStart = set(string.ascii_uppercase)

    # Methods
    @classmethod
    def initFromEnv(cls):
        """Initializes config from environment variables or defaults."""
        if not cls.envInitialized:
            env, envMap, envDefaults = cls.env, cls.envMap, cls.envDefaults
            for key in envMap:
                setattr(cls, key, env.get(envMap[key], envDefaults[key]) if key in envDefaults
                    else env[envMap[key]])
            cls.envInitialized = True
            cls.log('initialized {} config'.format(cls.ENV))

        return cls

    @classmethod
    def select(cls, key=None):
        """Returns selected environment configuration."""
        selectKey = key or getattr(cls, cls.envSelectProperty)
        selectClass = cls.getClassName(selectKey)

        config = getattr(cls.namespace, selectClass, cls)

        if config.genericActiveConfigName:
            setattr(config.namespace, config.genericActiveConfigName, config)

        return config

    @classmethod
    def update(__cls__, __settings__=None, **settings):
        """Updates configuration from dictionary and/or keyword arguments."""
        if (__settings__):
            __settings__.update(settings)
        else:
            __settings__ = settings

        for key in __settings__:
            setattr(__cls__, key, __settings__[key])

        return __cls__

    @classmethod
    def isKey(cls, key):
        """Tests if key is a valid configuration value key.

        Valid keys do start with uppercase character.
        """
        return key and key[0] in cls.envKeyStart

    @classmethod
    def isConfig(cls, config):
        """Tests if config is a valid configuration class.

        Valid configuration classes are subclasses of Config.root.
        """
        return isinstance(config, type) and issubclass(config, cls.root)

    @classmethod
    def getClassName(cls, envName):
        """Returns a configuration class name for given configuration environment name."""
        return envName.capitalize() + 'Config'

    @classmethod
    def getEnvName(cls, className):
        """Returns a configuration environment name for given configuration class name."""
        return className.replace('Config', '').lower()

    @classmethod
    def log(cls, message):
        """Logging method placeholder."""
        pass

def createConfig(namespace=None, updateEnv=None, updateEnvMap=None, updateEnvHelp=None, updateEnvDefaults=None,
    config=Config, initFromEnv=True, **settings):
    """Creates a base configuration class."""
    namespace = sys.modules[namespace] if isinstance(namespace, str) else namespace

    class Config(config):
        configurationsNamespace = namespace

    Config.root = Config

    Config.update(settings)

    if updateEnv:
        Config.env.update(updateEnv)

    if updateEnvMap:
        Config.envMap.update(updateEnvMap)

    if updateEnvHelp:
        Config.envHelp.update(updateEnvHelp)

    if updateEnvDefaults:
        Config.envDefaults.update(updateEnvDefaults)

    if initFromEnv:
        Config.initFromEnv()

    return Config
