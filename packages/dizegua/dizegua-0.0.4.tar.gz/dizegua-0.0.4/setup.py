from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Esse pacote só diz égua'
LONG_DESCRIPTION = DESCRIPTION

setup(
        name="dizegua",
        version=VERSION,
        author="Thalyson Wilker",
        author_email="thalison.wilker@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)