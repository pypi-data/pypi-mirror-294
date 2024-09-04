from setuptools import setup, find_packages

DESCRIPTION = "This python module do nothing but print \"ayw NB\" as \"import ayw as nb\", and \"nb\" at simple import."
VERSION = "0.0.4"

setup(name="ayw",
      version=VERSION,
      description=DESCRIPTION,
      url="https://github.com/FranklinBao/ayw",
      packages=find_packages(),
      classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers"
      ]
      )