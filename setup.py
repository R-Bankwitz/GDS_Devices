import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GDS_Devices", # Replace with your own username
    version="0.1.0",
    author="Rasmus Bankwitz",
    author_email="j_bank02@wwu.de",
    description="GDS Devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/R-Bankwitz/GDS-Devices.git",
    packages=["GDS_Devices"],
    package_dir={'': '.'},
    #package_data={'': ['remoteSolver/fdfd/cpp/fdfdSimBridge*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)