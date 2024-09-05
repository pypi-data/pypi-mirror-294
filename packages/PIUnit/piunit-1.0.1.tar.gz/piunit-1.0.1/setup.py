from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='PIUnit',
  version='1.0.1',
  author='MChekashov',
  author_email='chekashovmatvey@gmail.com',
  description='Library for convenient code testing with print and input functions',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Ryize/PIUnit',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'Operating System :: OS Independent'
  ],
  keywords='python test unittest print input',
  project_urls={
    'Documentation': 'https://github.com/Ryize/PIUnit'
  },
  python_requires='>=3.7'
)