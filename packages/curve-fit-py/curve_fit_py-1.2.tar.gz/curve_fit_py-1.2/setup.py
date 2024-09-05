import pathlib
import setuptools

setuptools.setup(
    name="curve_fit_py",
    version="1.2",
    description="A package for fitting a curve given an array of data points",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url = " ",
    author="Giovanni Paiela",
    author_email="jovpa47@gmail.com",
    license="MIT",
    project_urls={
        "Source": "https://github.com/Paiela/curve_fit_py"
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    python_requires=">= 3.11.4",
    install_requires=["numpy"],
    packages = setuptools.find_packages(),
    include_package_data=True,
)