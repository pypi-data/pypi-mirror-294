# setup.py
from setuptools import setup, find_packages

setup(
    name="asm_api_lib",
    version="1.2.1",
    packages=find_packages(include=['asm_api_lib']),
    install_requires=[],
    setup_requires=['pytest-runner'],
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
    # url="https://github.com/yourusername/asm_api_lib",
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    python_requires='>=3.6',
)