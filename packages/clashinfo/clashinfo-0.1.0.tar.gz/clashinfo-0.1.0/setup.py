from setuptools import setup, find_packages

setup(
    name="clashinfo",
    version="0.1.0",
    description="A Python wrapper for the Clash of Clans and Clash Royale API",
    author="Agilarasu Saravanan",
    author_email="s.agilarasu@outlook.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        # dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
