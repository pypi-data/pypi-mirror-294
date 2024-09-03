from setuptools import setup, find_packages

setup(
    name="patchshuffler",
    version="0.1.0",
    author="Jaeho Kim",
    author_email="jaeho3690@gmail.com",
    description="A package for shuffling patches in time series patched data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaeho3690/patchshuffler",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch",
        "numpy",
        "pandas",
        "einops",
    ],
)