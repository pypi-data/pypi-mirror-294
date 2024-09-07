from setuptools import setup, find_packages
import SBDL

NAME = "sbdletldemo"
DESCRIPTION = "Package of SBDL app"
LONG_DESCRIPTION = ""

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=SBDL.__author__,
    version=SBDL.__version__,
    author_email="akash967049@gmail.com",
    packages=["SBDL"],
    install_requires=["setuptools"],
    entry_points={
        "group_1":"run=SBDL.__main__:from_databricks"
    },
    keywords=['python', 'etl', 'boiler', 'local', 'databricks']
)