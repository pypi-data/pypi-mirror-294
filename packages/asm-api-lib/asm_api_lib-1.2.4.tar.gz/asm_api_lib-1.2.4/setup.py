# setup.py
from setuptools import setup, find_packages

# Right now this library is hosted in my personal PyPi account

setup(
    name="asm_api_lib",
    version="1.2.4",
    packages=find_packages(include=['asm_api_lib']),
    install_requires=[],
    setup_requires=['pytest-runner', 'pytest'],
    extras_require={
      'test': [
            'pytest==4.4.1'
        ],
    },
    test_suite='test',
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for AsmApi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)