from setuptools import find_packages, setup


def get_long_description():
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

    return long_description


setup(
    name="sbatch_paramfile",
    version="0.1.1",
    author="Wissam Antoun",
    author_email="wissam.antoun@gmail.com",
    description="A command line tool to create a sbatch file for a parameter file",
    long_description=get_long_description(),
    url="https://github.com/WissamAntoun/sbatch_paramfile",
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "sbatch_paramfile = sbatch_paramfile.main:entry_point",
        ],
    },
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
)
