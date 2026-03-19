from setuptools import setup, find_packages

setup(
    name="p2p-copy",
    version="1.1.0",
    author="Jose Falcón",
    author_email="josefalcon@gmail.com",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "p2p-copy=p2p_copy.cli:main",
        ],
    },
)
