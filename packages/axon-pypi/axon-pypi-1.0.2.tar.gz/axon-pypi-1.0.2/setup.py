from setuptools import setup, find_packages
import os
import codecs

current_dir = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(current_dir, "README.md"), encoding="utf-8") as file:
  long_description = file.read()

VERSION = '1.0.2'
DESCRIPTION = 'Multi-dimensional array creation & manipulation library like numpy written from scratch in python along with a scalar level autograd engine written in C/C++ with python wrapper'
lib_path = os.path.join(current_dir, 'axon', 'micro', 'libscalar.so')

if not os.path.exists(lib_path):
  raise FileNotFoundError(f"Shared library {lib_path} not found. Please compile the C++ code to generate libscalar.so")

setup(
  name="axon-pypi",
  version=VERSION,
  author="shivendra",
  author_email="shivharsh44@gmail.com",
  description=DESCRIPTION,
  long_description=long_description,
  long_description_content_type="text/markdown",
  license="MIT",
  packages=find_packages(include=['axon', 'axon.*']),
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Programming Language :: C",
    "Programming Language :: C++",
    "Programming Language :: Python :: 3.11",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
  ],
  package_data={
    'axon.micro': ['libscalar.so', '*.h', '*.cpp'],
    'axon': ['dtypes/*.py', 'helpers/*.py']
  },
  include_package_data=True,
  entry_points={
    'console_scripts': [
      'axon=axon.__main__:main',
    ],
  }
)