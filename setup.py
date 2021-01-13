import setuptools

with open('README.md') as fl:
    l_desc = fl.read()

setuptools.setup(
    name="pyNetSocket",
    version="1.0.7",
    author="DrSparky-2007",
    author_email="adityaiyer2007@gmail.com",
    description="A simple networking library for python",
    long_description=l_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/DrSparky-2007/PyNetSocket",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        'networking',
        'sockets',
        'simple networking',
        'simple sockets',
        'pyNetSockets',
        'pyNetSocket'
    ],
    python_requires='>=3.6'
)
