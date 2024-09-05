from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='wessql',
  version='0.0.2',
  author='w3ssel',
  author_email='johnywessel@gmail.com',
  description='This is the simplest module for quick work with sqlite3.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/JohnyWessel/simple-database',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='wessql',
  project_urls={
    'GitHub': 'https://github.com/johnywessel'
  },
  python_requires='>=3.1.1'
)