from setuptools import setup, find_packages

README_FILE = open('README.md', 'r')
README = README_FILE.read()
README_FILE.close()

setup(
    name='htto',
    version='1.0',
    author='osmz',
    description='simple, high performance http requests library',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://www.github.com/xsxo/htto',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ]
)