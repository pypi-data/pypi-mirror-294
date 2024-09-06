from re import findall
from setuptools import setup, find_packages


with open("miftahdb/__init__.py", "r") as f:
    version = findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.md", "r") as f:
    readme = f.read()


setup(
    name="miftahdb",
    version=version,
    description="Easy-to-use synchronous/asynchronous key-value database backed by sqlite3.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="vwh",
    author_email="vwhe@proton.me",
    url="https://github.com/miftahDB/miftahdb-python",
    license="MIT",
    python_requires=">=3.8",
    project_urls={
        "Source": "https://github.com/miftahDB/miftahdb-python",
        "Tracker": "https://github.com/miftahDB/miftahdb-python/issues",
        "Documentation": "https://miftahdb.rtfd.io/",
    },
    packages=find_packages(exclude=["docs"]),
    keywords=[
        "sync",
        "asyncio",
        "sqlite",
        "sqlite3",
        "key-value",
        "database",
        "redis",
    ],
)
