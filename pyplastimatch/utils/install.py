"""
    ----------------------------------------
    PyPlastimatch
    
    Setup utility function
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dbontempi@bwh.harvard.edu
    ----------------------------------------
    
"""

import os
import sys
import shutil

import json
import requests
import urllib.request

import subprocess

import tempfile

def get_distro_info():
  """
  Get the distribution info of the current system from "/etc/os-release"
  formatted in a dictionary fashion.
  """

  # check if the file exists
  if not os.path.exists("/etc/os-release"):
    raise FileNotFoundError("The file '/etc/os-release' does not exist.")

  # read the file
  with open("/etc/os-release", "r") as f:
    lines = f.readlines()

  # parse the file
  distro_info_dict = dict()

  for line in lines:
    key, val = line.replace("\n", "").split("=")
    
    # make the key lowercase
    key = key.lower()

    # if "val" is a string that starts end ends with quotes, remove them
    if val[0] == '"':
      val = val[1:-1]
    distro_info_dict[key] = val

  return distro_info_dict

## --------------------------------

def install_binaries(binaries_path: str) -> None:

  # copy the binaries to the right folder
  print("\nInstalling binaries...", end="")
  shutil.copy(binaries_path, "/usr/local/bin/plastimatch")
  
  # make the file executable
  subprocess.run(["chmod", "+x", "/usr/local/bin/plastimatch"])
  print(" Done.")

  # install dependencies
  print("Installing dependencies...", end="")
  install_dependencies()
  print(" Done.")
  
## --------------------------------

def install_dependencies() -> None:
  subprocess.run(["apt-get", "update"])
  subprocess.run(["apt-get", "install", "-y", "libinsighttoolkit4-dev", "libdcmtk16", "libdlib19", "libfftw3-dev"])

## --------------------------------

def download_binaries() -> str:
  """
  Download the plastimatch binaries compiled for the specified distribution (if found).
  
  The information regarding the distribution is automatically parsed from "/etc/os-release"
  as a dictionary by the get_distro_info() function.

  Returns:
      str: path to the downloaded binaries, and info on the download status
  """
  
  distro_info_dict = get_distro_info()
  
  # get the distribution info
  distro_name = distro_info_dict["name"]
  distro_version_id = distro_info_dict["version_id"]

  # to check if the distribution is supported, check the build_release.json file in the repo
  # read the build_release.json file from the utils directory
  build_release_path = os.path.join(os.path.dirname(__file__), "build_release.json")
  with open(build_release_path, "r") as f:
    build_release_dict = json.load(f)
  
  print("System distribution: %s %s"%(distro_name, distro_version_id))

  supported = False

  # check if the distribution is supported
  for supported_distro_key in build_release_dict.keys():
    supported_distro = build_release_dict[supported_distro_key]
    if distro_name == supported_distro["name"] and \
       distro_version_id == supported_distro["version_id"]:
      
      supported = True
      break

  if supported:
    print("Matching distribution found in the latest PyPlastimatch release.")
  else:
    print("You system does not have a compiled binary in the latest PyPlastimatch release.")

  releases_url = "https://api.github.com/repos/AIM-Harvard/pyplastimatch/releases"
  releases_dict = requests.get(releases_url).json()

  # get the latest release
  for release in releases_dict:
    release["tag_name"] == "latest"
    latest_release_dict = release

  # look for the right asset
  assets_list = latest_release_dict["assets"]
  
  # the asset name is always going to be formatted as "plastimatch-$OS_${MAJOR_VERSION}_${MINOR_VERSION}"
  distro_asset_name = "plastimatch-%s_%s_%s"%(
    distro_name.lower(),
    distro_version_id.split(".")[0],
    distro_version_id.split(".")[1]
    )

  for asset in assets_list:
    if asset["name"] == distro_asset_name:
      distro_asset = asset
      break
  
  # download the asset
  browser_download_url = distro_asset["browser_download_url"]
  
  temp_dir = tempfile.TemporaryDirectory()
  filename = os.path.join(temp_dir.name, distro_asset_name)
  
  print("\nDownloading binary in the temp directory %s..."%filename, end="")
  print(" Done.")
  
  urllib.request.urlretrieve(browser_download_url, filename)

  install_binaries(filename)

  temp_dir.cleanup()

  return None