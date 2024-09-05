
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_rss",
    version="1.2",
    author="Michael Mondoro",
    author_email="michaelmondoro@gmail.com",
    description="Simple Python package for interacting with RSS feeds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaelMondoro/easy_rss",
    packages=setuptools.find_packages(exclude="tests"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pytz', 'bs4', 'requests'],
    python_requires='>=3.8',
)
