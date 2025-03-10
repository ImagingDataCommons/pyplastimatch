"""
    ----------------------------------------
    PyPlastimatch
    
    dummy python plastimatch wrapper
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dbontempi@bwh.harvard.edu
    ----------------------------------------
    
"""

import os
import json
import subprocess
from typing import Dict

## ----------------------------------------

# FIXME: like this, every command is basically the same function with a line changed
# define classes/something more fancy (for parsing etc.)?
# Otherwise we may very well just have a function called "run_plastimatch_command"
# and pass it also the command we want to run (convert, resample, etc.)

def convert(verbose = True, path_to_log_file = None, return_bash_command = False, **kwargs):
  """
  Convert DICOM series to any supported file format.
  
  For additional details, see:
  https://plastimatch.org/plastimatch.html#plastimatch-convert
  
  Args:
      (GENERAL)
      path_to_log_file: path to file where stdout and stderr from the processing should be logged
      return_bash_command: return the executed command together with the exit status
      
      **kwargs: all the arguments parsable by 'plastimatch convert'
        Special Cases:
            - metadata (list): If provided as a list, each item is passed as a separate `--metadata` argument.
  """

  bash_command = list()
  bash_command += ["plastimatch", "convert"]
  
  for key, val in kwargs.items():
      if key == "metadata" and isinstance(val, list):
          for meta in val:
              bash_command += ["--metadata", str(meta)]
      else:
          bash_command += [f"--{key}", str(val)]
  
  if verbose:
    print("\nRunning 'plastimatch convert' with the specified arguments:")
    for arg in bash_command[2:]:
        print(f"  {arg}")
  
  try:
    if path_to_log_file:
      with open(path_to_log_file, "a") as log_file:
        bash_exit_status = subprocess.run(bash_command,
                                          stdout = log_file, stderr = log_file,
                                          check = True)
    else:
      # if no log file is specified, output to the default stdout and stderr
      bash_exit_status = subprocess.run(bash_command, capture_output = True, check = True)
      
    if verbose: print("... Done.")
    
  except Exception as e:
    # if the process exits with a non-zero exit code, a CalledProcessError exception will be raised
    # attributes of that exception hold the arguments, the exit code, and stdout and stderr if they were captured
    # For details, see: https://docs.python.org/3/library/subprocess.html#subprocess.run
    
    # FIXME: return exception?
    print(e)
  
  if return_bash_command:
    return bash_command

## ----------------------------------------

def resample(verbose = True, path_to_log_file = None, return_bash_command = False, **kwargs):
  """
  Resample any volume of a supported format.
  
  For additional details, see:
  https://plastimatch.org/plastimatch.html#plastimatch-resample
  
  Args:
      (GENERAL)
      path_to_log_file: path to file where stdout and stderr from the processing should be logged
      return_bash_command: return the executed command together with the exit status
      
      **kwargs: all the arguments parsable by 'plastimatch resample'
      
  """
  
  bash_command = list()
  bash_command += ["plastimatch", "resample"]
  
  for key, val in kwargs.items():
    bash_command += ["--%s"%(key), val]
  
  if verbose:
    print("\nRunning 'plastimatch resample' with the specified arguments:")
    for key, val in kwargs.items():
      print("  --%s"%(key), val)
  
  try:
    if path_to_log_file:
      with open(path_to_log_file, "a") as log_file:
        bash_exit_status = subprocess.run(bash_command,
                                          stdout = log_file, stderr = log_file,
                                          check = True)
    else:
      # if no log file is specified, output to the default stdout and stderr
      bash_exit_status = subprocess.run(bash_command, capture_output = True, check = True)
      
    if verbose: print("... Done.")
    
  except Exception as e:
    # if the process exits with a non-zero exit code, a CalledProcessError exception will be raised
    # attributes of that exception hold the arguments, the exit code, and stdout and stderr if they were captured
    # For details, see: https://docs.python.org/3/library/subprocess.html#subprocess.run
    
    # FIXME: return exception?
    print(e)
  
  if return_bash_command:
    return bash_command
  
## ----------------------------------------

def dice(path_to_reference_img, path_to_test_img, verbose = True):
  """
  Compute Dice coefficient for binary label images.
  
  For additional details, see:
  https://plastimatch.org/plastimatch.html#plastimatch-dice
  
  Args:
      path_to_reference_img:
      path_to_test_img:
      
  Returns:
      dice_summary_dict:
     
  """
  
  bash_command = list()
  bash_command += ["plastimatch", "dice", "--dice"]
  bash_command += [path_to_reference_img, path_to_test_img]
  
  if verbose: print("\nComputing DC between the two images with 'plastimatch dice --dice'")
  
  try:
    dice_summary = subprocess.run(bash_command, capture_output = True, check = True)
    if verbose: print("... Done.")
  except Exception as e: 
    # if the process exits with a non-zero exit code, a CalledProcessError exception will be raised
    # attributes of that exception hold the arguments, the exit code, and stdout and stderr if they were captured
    # For details, see: https://docs.python.org/3/library/subprocess.html#subprocess.run
    
    # FIXME: return exception?
    print(e)
     
  dice_summary = dice_summary.stdout.decode().splitlines()
  
  dice_summary_dict = dict()
  dice_summary_dict["com"] = dict()

  dice_summary_dict["com"]["ref"] = [float(dice_summary[1].split("\t")[1]),
                                     float(dice_summary[1].split("\t")[2]),
                                     float(dice_summary[1].split("\t")[3])]

  dice_summary_dict["com"]["cmp"] = [float(dice_summary[2].split("\t")[1]),
                                     float(dice_summary[2].split("\t")[2]),
                                     float(dice_summary[2].split("\t")[3])]

  dice_summary_dict["dc"] = float(dice_summary[7].split(":")[1])
  
  return dice_summary_dict
  
## ----------------------------------------


def hd(path_to_reference_img, path_to_test_img, verbose = True):
  """
  Compute Hausdorff Distance for binary label images.
  
  For additional details, see:
  https://plastimatch.org/plastimatch.html#plastimatch-dice
  
  Args:
      path_to_reference_img:
      path_to_test_img:
      return_bash_command: return the executed command together with the exit status
     
  """
  
  bash_command = list()
  bash_command += ["plastimatch", "dice", "--hausdorff"]
  bash_command += [path_to_reference_img, path_to_test_img]
  
  if verbose: print("\nComputing the HD between the two images with 'plastimatch dice --hausdorff'")
  
  try:
    hausdorff_summary = subprocess.run(bash_command, capture_output = True, check = True)
    if verbose: print("... Done.")
  except Exception as e: 
    # if the process exits with a non-zero exit code, a CalledProcessError exception will be raised
    # attributes of that exception hold the arguments, the exit code, and stdout and stderr if they were captured
    # For details, see: https://docs.python.org/3/library/subprocess.html#subprocess.run
    
    # FIXME: return exception?
    print(e)
  
  hausdorff_summary = hausdorff_summary.stdout.decode().splitlines()
  
  hausdorff_summary_dict = dict()

  hausdorff_summary_dict["hd"] = float(hausdorff_summary[0].split("=")[-1])
  hausdorff_summary_dict["hd95"] = float(hausdorff_summary[3].split("=")[-1])
  
  hausdorff_summary_dict["hd_boundaries"] = float(hausdorff_summary[4].split("=")[-1])
  hausdorff_summary_dict["hd95_boundaries"] = float(hausdorff_summary[-1].split("=")[-1])
  
  return hausdorff_summary_dict

## ----------------------------------------

def compare(path_to_reference_img, path_to_test_img, verbose = True) -> Dict[str, float]:
  """
  The compare command compares two files by subtracting one file from the other, and reporting statistics of the difference image. 
  The two input files must have the same geometry (origin, dimensions, and voxel spacing). The command line usage is given as follows:
  
  For additional details, see:
  https://plastimatch.org/plastimatch.html#plastimatch-compare
  
  Args:
      path_to_reference_img:
      path_to_test_img:
      
  Returns:
      dictionary:
        MIN      Minimum value of difference image
        AVE      Average value of difference image
        MAX      Maximum value of difference image
        MAE      Mean average value of difference image
        MSE      Mean squared difference between images
        DIF      Number of pixels with different intensities
        NUM      Total number of voxels in the difference image
     
  """
  
  # print
  if verbose: 
    print("\n Comparing two images with 'plastimatch compare'")

  # build command
  bash_command = []
  bash_command += ["plastimatch", "compare"]
  bash_command += [path_to_reference_img, path_to_test_img]
  
  # run command
  dice_summary = subprocess.run(bash_command, capture_output = True, check = True)
  
  # print
  if verbose: 
    print("... Done.")

  # combine output
  comparison_raw = dice_summary.stdout.decode('utf-8')

  # flaten output
  comparison_flat = " ".join(comparison_raw.splitlines()).split()
  assert len(comparison_flat) == 14, "Unfamiliar output."
  
  # parse output into dictionary
  comparison_dict = {}
  for i in range(0, len(comparison_flat), 2):
    comparison_dict[comparison_flat[i]] = float(comparison_flat[i+1])
    
  # return dictionary
  return comparison_dict

## ----------------------------------------
