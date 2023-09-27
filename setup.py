from setuptools import setup

setup(name="pyplastimatch",
      version="0.1",
      description="Basic Python wrapper for Plastimatch",
      url="https://github.com/AIM-Harvard/pyplastimatch",
      author="AIM-Harvard",
      license="GNU General Public License, Version 3.0",
      packages=["pyplastimatch", "pyplastimatch.utils"],
      install_requires=["numpy", "scikit-image>=0.14",
			"SimpleITK", "pydicom", "pandas", "matplotlib", "requests"])
