from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Package for video processing.'
LONG_DESCRIPTION = 'A one stop package for everything related to video processing.'

# Setting up
setup(
    name="videogram",
    version=VERSION,
    author="Ishan Dutta",
    author_email="duttaishan0098@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video processing', 'video editing', 'video recording'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)