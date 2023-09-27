from setuptools import setup

setup(
  name="pyplastimatch",
  version="0.2",
  description="Basic Python wrapper for Plastimatch",
  url="https://github.com/AIM-Harvard/pyplastimatch",
  author="Dennis Bontempi",
  license=" BSD-3-Clause license",
  packages=[
    "pyplastimatch",
    "pyplastimatch.utils"
    ],
  install_requires=[
        "numpy",
        "scikit-image>=0.14",
        "SimpleITK",
        "pydicom",
        "pandas",
        "matplotlib",
        "requests"
        ]
        )
