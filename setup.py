import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "nxtools",
    version = "1.0.0",
    author = "Martin Wacker",
    author_email = "martas@imm.cz",
    description = "Set of common utilities and little helpers.",
    license = "MIT",
    keywords = "utilities log logging ffmpeg watchfolder media mam time",
    url = "https://github.com/immstudios/nxtools",
    packages=['nxtools', 'nxtools.media', 'nxtools.caspar'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Utilities",
    ],
)
