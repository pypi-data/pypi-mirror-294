from setuptools import setup, find_packages

setup(
    name="checkexplore-defect-package",
    version="0.1.0",
    author="Checkexplore",
    author_email="deepkumar.patel@checkexplore.com",
    description="A brief description of your package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True,
)
