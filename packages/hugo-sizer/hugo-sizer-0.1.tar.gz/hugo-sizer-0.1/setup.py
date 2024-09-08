# setup.py
from setuptools import setup

setup(
    name='hugo-sizer',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        "requests >= 2.31.0",
        "aiohttp >= 3.10.5",
        "aiohttp >= 3.10.5",
        "beautifulsoup4 >= 4.12.2"
    ],
    entry_points={
        'console_scripts': [
            'hugo-sizer=cli:main',  # This maps `my-tool` command to `main` function in `my_tool.py`
        ],
    },
)
