from setuptools import setup

setup(name='Hoover',
      version='0.1',
      description="Library for logging to Loggly from within Python webapps",
      author="Mike Blume",
      author_email="mike@loggly.com",
      # fix this
      url="http://www.loggly.com",
      packages=['hoover'],
      install_requires=['httplib2'],
)
