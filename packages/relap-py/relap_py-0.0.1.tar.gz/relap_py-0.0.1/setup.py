from setuptools import setup, find_packages
import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    # long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Module for RELAP post-processing'

# Setting up
setup(
    name="relap_py",
    version=VERSION,
    author="Jordi Freixa",
    author_email="<jordi.freixa-terradas@upc.edu>",
    description=DESCRIPTION,
    # long_description_content_type="text/markdown",
    # long_description=long_description,
    packages=find_packages(),
    # install_requires=['os', 'matplotlib'],
    keywords=['relap', 'trace']
)
