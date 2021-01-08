import setuptools

with open('README.md') as fl:
    l_desc = fl.read()

setuptools.setup(
    name="PySimSockets",
    version="1.0.0",
    author="DrSparky-2007",
    author_email="adityaiyer2007@gmail.com",
    description="A simple networking library for python",
    long_description=l_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/DrSparky-2007/PySimpleSockets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keys=[
        'networking',
        'sockets',
        'simple networking',
        'simple sockets'
    ],
    python_requires='>=3.6'
)
