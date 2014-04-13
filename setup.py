from setuptools import setup, find_packages
from os.path import dirname, realpath, join


CURRENT_DIR = dirname(realpath(__file__))

with open(join(CURRENT_DIR, "README.rst")) as long_description_file:
    long_description = long_description_file.read()

with open(join(CURRENT_DIR, "flask_navigation/__init__.py")) as package_file:
    version = next(eval(line.split("=")[-1])
                   for line in package_file if line.startswith("__version__"))


setup(
    name="Flask-Navigation",
    packages=find_packages(exclude=["tests", "docs"]),
    version=version,
    description="The navigation of Flask application.",
    long_description=long_description,
    author="Jiangge Zhang",
    author_email="tonyseek@gmail.com",
    url="https://github.com/tonyseek/flask-navigation",
    license="MIT",
    keywords=["navigation", "flask", "navbar", "nav"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=["Flask", "blinker"],
)
