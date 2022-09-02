import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="PyMAL",
    version="0.0.1",
    author="Raditya Harya",
    author_email="radityaharya02@gmail.com",
    description="A Python wrapper for MyAnimeList API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/radityaharya/PyMAL",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "flask",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
