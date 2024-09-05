# Import necessary functions from setuptools to configure the package
from setuptools import find_packages, setup

# Open the README.md file in read mode to include it as the long description of the package
with open("README.md", "r") as f:
    long_description = f.read()  # Read the entire content of the file and store it in long_description

# The setup function is used to specify details about the package
setup(
    name="auto-synth-data-gen",  # The name of the package as it will appear in PyPI
    version="0.0.3",  # Initial version of the package (follows semantic versioning)
    description="A Python package to generate synthetic datasets resembling real-world data",  # Short description of what the package does

    # Define the directory structure; here, 'app' is the root folder containing the package
    package_dir={"": "app"},  
    # Automatically find all sub-packages within the 'app' directory
    packages=find_packages(where="app"),

    # Long description is typically the content of README.md for detailed documentation
    long_description=long_description,  
    # Specify that the long description is written in markdown format
    long_description_content_type="text/markdown",

    # URL to the GitHub repository where the package's source code is hosted
    url="https://github.com/Gouranga-GH/custom_pypi_sdg.git",  

    # Information about the package author
    author="Gouranga Jha",  
    # Contact email for the package author
    author_email="post.gourang@gmail.com",  

    # License information for the package (here, the MIT license is used)
    license="MIT",  
    
    # Classifiers help users and PyPI categorize the package
    classifiers=[
        # The license under which the package is distributed
        "License :: OSI Approved :: MIT License",
        # The Python version compatibility
        "Programming Language :: Python :: 3",
        # The package is platform-independent (works on all operating systems)
        "Operating System :: OS Independent",
    ],

    # The external dependencies (libraries) that need to be installed for the package to work
    install_requires=["numpy >= 1.24.4", "pandas >= 2.0.3"],

    # Additional optional dependencies for development and testing
    extras_require={
        "dev": ["pytest>=7.0", "twine>=5.1.1"],  # 'dev' extras include packages for running tests and uploading to PyPI
    },

    # Specifies the minimum required Python version for using the package
    python_requires=">=3.8",
)
