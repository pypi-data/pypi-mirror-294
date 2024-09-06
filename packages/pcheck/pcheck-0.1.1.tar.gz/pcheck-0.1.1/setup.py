from setuptools import setup, find_packages

setup(
    name='pcheck',
    version='0.1.1',

    author="CodingLive",
    author_email="rootcode@duck.com",
    description="A easy to use and blazingly fast proxy checker written in python ",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ProtDos/pcheck",

    packages=find_packages(),
    install_requires=[
        'aiohttp',
    ],
    entry_points={
        'console_scripts': [
            'pcheck=pcheck.__main__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
