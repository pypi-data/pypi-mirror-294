from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='movoid_timer',
    version='1.0.4',
    packages=find_packages(),
    url='',
    license='',
    author='movoid',
    author_email='bobrobotsun@163.com',
    description='create timer to record time',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
)
