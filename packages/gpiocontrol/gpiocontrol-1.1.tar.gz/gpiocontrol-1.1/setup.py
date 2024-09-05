from setuptools import setup, find_packages

setup(
    name='gpiocontrol',
    version='1.1',
    description="Simple wrapper for bash commands to control GPIO.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='s17kf',
    packages=find_packages(),
)
