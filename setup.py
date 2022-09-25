from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='flyby',
      version='0.0.1',
      author="Mingde Yin",
      description="Multi-Gravity Assist Interplanetary Transfer Optimization Tool.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="LGPLv3",
      packages=find_packages(),
      classifiers=["Development Status :: 3 - Alpha",
                   "Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: C",
                   "Topic :: Scientific/Engineering :: Physics",
                   "Intended Audience :: Science/Research"],
      python_requires='>=3.6')