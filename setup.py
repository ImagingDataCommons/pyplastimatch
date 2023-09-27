from setuptools import setup

setup(
  name="pyplastimatch",
  version="0.4.3",
  description="Basic Python wrapper for Plastimatch",
  url="https://github.com/AIM-Harvard/pyplastimatch",
  author="Dennis Bontempi",
  license=" BSD-3-Clause license",
  packages=[
    "pyplastimatch",
    "pyplastimatch.utils"
    ],
  install_requires=[
        "itk",
        "matplotlib",
        "numpy",
        "pandas",
        "pydicom",
        "requests",
        "scikit-image",
        "SimpleITK"
        ]
        )
