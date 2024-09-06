from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='treegear',
  version='0.0.0.1',
  author='Gyuli',
  author_email='guli.peradze@gmail.com',
  description='This module is for tests for future project.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  # url='treegear.dev',
  url='http://185.78.76.240',
  packages=find_packages(),
  install_requires=['uvicorn'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python uvicorn',
  project_urls={
    # 'Documentation': 'treegear.dev'
    'Documentation': 'http://185.78.76.240'
  },
  python_requires='>=3.8'
)