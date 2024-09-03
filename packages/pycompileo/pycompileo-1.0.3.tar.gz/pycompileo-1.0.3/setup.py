from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    readme = "\n" + fh.read()

VERSION = '1.0.3'  # Increment on next change
DESCRIPTION = 'Python Code Obfuscator.'

setup(
    name="pycompileo",
    version=VERSION,
    author="Schkimansky",
    author_email="<ahmadchawla1432@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=readme,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'compile', 'decompile', 'proprietarify', 'obfuscate', 'code', 'obfuscation'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
