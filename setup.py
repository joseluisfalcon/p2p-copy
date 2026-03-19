from setuptools import setup, find_packages

setup(
    name="p2p-copy",
    version="0.1.0",
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
