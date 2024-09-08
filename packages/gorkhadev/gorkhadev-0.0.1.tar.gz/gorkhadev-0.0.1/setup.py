from setuptools import setup, find_packages
from os import path

work_dir = path.abspath(path.dirname(__file__))

with open(path.join(work_dir, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='gorkhadev',
  version='0.0.1',
  url='https://github.com/gorkhadev/gorkhadev',
  author='Gorkha Dev',
  author_email='gorkhadeveloper@gmail.com',
  description='CLI for Gorkha Dev',
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=[],
)
