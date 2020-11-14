import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rayvis",
    version="0.0.3",
    author="Martin Sach",
    author_email="martin.sachin@gmail.com",
    description="Tool to visualize various mesh files and more provided by raytracer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SachCZ/rayvis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    install_requires=[
        "matplotlib",
        "numpy",
        "vtk",
        "msgpack",
        'dataclasses'
    ]
)