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

def move_binaries(binaries_path: str, verbose: bool) -> None:

  # copy the binaries to the right folder
  print("\nInstalling binaries...", end="")
  shutil.copy(binaries_path, "/usr/local/bin/plastimatch")
  
  # make the file executable
  subprocess.run(["chmod", "+x", "/usr/local/bin/plastimatch"])
  print(" Done.")

  # install dependencies
  print("Installing dependencies...", end="")
  sys.stdout.flush()
  install_dependencies(verbose=verbose)
  print(" Done.")
  
## --------------------------------

def install_dependencies(verbose: bool) -> None:

  apt_update = ["apt-get", "update"]
  
  if verbose:
    subprocess.run(apt_update, capture_output=verbose, check=True)
  else:
    subprocess.run(
      apt_update,
      stdout=subprocess.DEVNULL,
      stderr=subprocess.STDOUT
      )
    

  dependency_list = ["libinsighttoolkit4-dev", "libdcmtk16", "libdlib19", "libfftw3-dev"]
  apt_install = ["apt-get", "install", "-y"] + dependency_list
  
  if verbose:
    subprocess.run(apt_install, capture_output=verbose, check=True)
  else:
    subprocess.run(
      apt_install,
      stdout=subprocess.DEVNULL,
      stderr=subprocess.STDOUT
      )

## --------------------------------

def install_precompiled_binaries(verbose: bool=False) -> None:
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

  print("PyPlastimatch Plastimatch installation utility.")
  print("NOTE: this utility is not meant to be replace the normal install of Plastimatch via apt.")
  print("Rather, it is meant to be used in case a Plastimatch binary is not available for a specific distribution.")
  print("\nSystem distribution: %s %s"%(distro_name, distro_version_id))

  releases_url = "https://api.github.com/repos/AIM-Harvard/pyplastimatch/releases"
  releases_dict = requests.get(releases_url).json()

  # request temp dir for the pull of the github release
  # (the directory will be deleted at upon exit from the function)
  temp_dir = tempfile.TemporaryDirectory()

  # get the latest release
  for release in releases_dict:
    release["tag_name"] == "latest"
    latest_release_dict = release

  # get the list of files in the release
  assets_list = latest_release_dict["assets"]

  # to check if the distribution is supported, check the release_meta.json file in the release
  meta_asset_name = "release_meta.json"

  # look for the release_meta.json file
  for asset in assets_list:
    if asset["name"] == meta_asset_name:
      meta_asset = asset
      break

  # download the file
  meta_browser_download_url = meta_asset["browser_download_url"]
  path_to_meta_json = os.path.join(temp_dir.name, meta_asset_name)

  print("\nDownloading meta JSON in the temp directory %s..."%path_to_meta_json, end="")
  print(" Done.")
  
  urllib.request.urlretrieve(meta_browser_download_url, path_to_meta_json)

  with open(path_to_meta_json, "r") as f:
    build_release_dict = json.load(f)
  
  # check if the distribution is supported
  supported = False

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
  path_to_binaries = os.path.join(temp_dir.name, distro_asset_name)
  
  print("\nDownloading binary in the temp directory %s..."%path_to_binaries, end="")
  print(" Done.")
  
  urllib.request.urlretrieve(browser_download_url, path_to_binaries)
  
  move_binaries(path_to_binaries, verbose=verbose)

  temp_dir.cleanup()