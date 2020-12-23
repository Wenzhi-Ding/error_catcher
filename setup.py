import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="error_catcher",
    version="0.1",
    author="Wenzhi Ding",
    author_email="wenzhi.ding@foxmail.com",
    description="A decorator to trace error and catch variables.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wenzhi-ding/error_catcher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)