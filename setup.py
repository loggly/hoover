try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from hoover.version import __version__

setup(name='Hoover',
      version=__version__,
      description="Library for logging to Loggly from within Python webapps",
      author="Mike Blume",
      author_email="mike@loggly.com",
      url="http://www.github.com/loggly/hoover",
      packages=['hoover'],
      install_requires=['httplib2'],
)
