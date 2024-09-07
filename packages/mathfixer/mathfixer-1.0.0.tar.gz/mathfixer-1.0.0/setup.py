from setuptools import *

setup(
    name="mathfixer",
    version="1.0.0",
    url="https://github.com/none-None1/mathfixer",
    py_modules=["mathfixer","proxy"],
    description="mathfixer, a tool for fixing math in MediaWiki-based wikis",
    long_description=open("README.md").read(),
    entry_points={"console_scripts": ["mathfixer=mathfixer:main"]},
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    long_description_content_type="text/markdown",
    requires=["mitmproxy","bs4"]
)
