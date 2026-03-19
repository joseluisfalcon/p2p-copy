from setuptools import setup, find_packages

setup(
    name="p2pc-secure",
    version="1.2.0",
    author="Jose Falcón",
    author_email="josefalcon@gmail.com",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "p2pc-secure=p2p_copy.cli:main",
        ],
    },
)
