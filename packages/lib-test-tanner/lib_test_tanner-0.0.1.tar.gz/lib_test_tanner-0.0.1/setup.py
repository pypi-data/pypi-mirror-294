import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'  
PACKAGE_NAME = 'lib_test_tanner'  
AUTHOR = 'Nicolás Reyes Gallardo' 
AUTHOR_EMAIL = 'nreyes@inconsulting.cl'  
URL = 'https://github.com/nreyes-py/lib_test'  

LICENSE = 'MIT'  
DESCRIPTION = 'Librería para pruebas y funciones en Databricks'  
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 
LONG_DESC_TYPE = "text/markdown"

# Dependencias necesarias para que funcione la librería
INSTALL_REQUIRES = [
    # 'pandas>=1.3',
    # 'numpy>=1.21',
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
