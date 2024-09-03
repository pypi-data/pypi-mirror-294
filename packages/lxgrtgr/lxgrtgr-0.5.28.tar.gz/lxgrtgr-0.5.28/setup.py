import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lxgrtgr",
    version="0.5.28",
    author="Kristopher Kyle",
    author_email="kristopherkyle1@gmail.com",
    description="Lexicogrammatical tagging and tag counting tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kristopherkyle/LxGrTgr",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=['importlib_resources'],
)