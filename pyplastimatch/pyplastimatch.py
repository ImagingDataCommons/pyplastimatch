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
from typing import Dict, List
from pathlib import Path
from collections import defaultdict
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
      
  """

  bash_command = list()
  bash_command += ["plastimatch", "convert"]
  
  for key, val in kwargs.items():
    bash_command += ["--%s"%(key), val]
  
  if verbose:
    print("\nRunning 'plastimatch convert' with the specified arguments:")
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

def register(
  global_params: Dict[str, str],
  stage_params_list: List[Dict[str, str]]
  ) -> Dict[str, float]:
  """
  Purpose:
    - To register two images using the plastimatch register command. The input to the command is a 
    text file called parm.txt. This text file has [Global] commands and [Stage] commands.
    While the variables for the global commands stay the same throughout many stages of the registration,
    the stage commands can be different for each stage. For the full list of these variables
    look at https://plastimatch.org/registration_command_file_reference.html.
    Here is an example of the parm.txt file:
      [GLOBAL]
      fixed=t5.mha
      moving=t0.mha
      image_out=warped.mha
      vf_out=deformation.nrrd

      [STAGE]
      xform=bspline
      grid_spac=50 50 50

      [STAGE]
      grid_spac=20 20 20

  Inputs:
    - global_params: dict := a dictionary containing the global parameters for the registration.
    The possible global parameters are:
      - fixed: str := the path to the fixed image.
      - moving: str := the path to the moving image.
      - fixed_roi: str := the path to the fixed region of interest.
      - moving_roi: str := the path to the moving region of interest.
      - fixed_landmarks: str := the path to the fixed landmarks.
      - moving_landmarks: str := the path to the moving landmarks.
      - warped_landmarks: str := the path to the warped landmarks.
      - xform_in: str := the path to the input transformation.
      - xform_out: str := the path to the output transformation.
      - vf_out: str := the path to the output vector field.
      - img_out: str := the path to the output image.
      - img_out_fmt: str := the format of the output image.
      - img_out_type: str := the type of the output image.
      - resample_when_linear: bool := whether to resample when linear.
      - logfile: str := the path to the log file.
    - stage_params_list: List[Dict[str, str]] := a list of dictionaries containing the stage parameters for the registration.
    please look at the plastimatch documentation for the full list of possible stage parameters.
  Outputs:
    - registration_summary: Dict[str, float] := a dictionary containing the registration summary.
    The possible keys are:
      - pth_registered_data: str := the path to the registered data.
      - log_file: str := the path to the log file.
  """
  
  # here are the possible global parameters for the registration
  # some are optional, some are mandatory, we loop through them 
  # and create the command
  global_param_possible_key_list = [
    "fixed", "moving", "fixed_roi",
    "moving_roi", "fixed_landmarks",
    "moving_landmarks","warped_landmarks",
    "xform_in", "xform_out", "vf_out",
    "image_out", "img_out_fmt", "img_out_type",
    "resample_when_linear", "logfile"
  ]
  final_global_params = defaultdict(str)
  # loop through the global parameters and create the command
  for key in global_params:
    if key in global_param_possible_key_list:
      final_global_params[key] = global_params[key]

  # make sure the required global parameters are present
  if "fixed" not in final_global_params:
    raise ValueError("The fixed image is required.")
  if "moving" not in final_global_params:
    raise ValueError("The moving image is required.")
  if "image_out" not in final_global_params:
    raise ValueError("The output image is required.")
  
  # here are the possible stage parameters for the registration
  # some are optional, some are mandatory, we loop through them
  # and create the command
  stage_param_possible_key_list = [
  "fixed_landmarks", "moving_landmarks", "warped_landmarks", "xform_out",
  "xform", "vf_out", "img_out", "img_out_fmt", "img_out_type",
  "resample_when_linear", "background_max", "convergence_tol", "default_value", 
  "demons_acceleration", "demons_filter_width", "demons_homogenization", "demons_std", 
  "demons_gradient_type", "demons_smooth_update_field", "demons_std_update_field",
  "demons_smooth_deformation_field", "demons_std_deformation_field", "demons_step_length",
  "grad_tol", "grid_spac", "gridsearch_min_overlap", "histoeq", "landmark_stiffness",
  "lbfgsb_mmax", "mattes_fixed_minVal", "mattes_fixed_maxVal", "mattes_moving_minVal",
  "mattes_moving_maxVal", "max_its", "max_step", "metric", "mi_histogram_bins", "min_its",
  "min_step", "num_hist_levels_equal", "num_matching_points", "num_samples", "num_samples_pct",
  "num_substages", "optim_subtype", "pgtol", "regularization", "diffusion_penalty", 
  "curvature_penalty", "linear_elastic_multiplier", "third_order_penalty", 
  "total_displacement_penalty", "lame_coefficient_1", "lame_coefficient_2", "res",
  "res_mm", "res_mm_fixed", "res_mm_moving", "res_vox", "res_vox_fixed",
  "res_vox_moving", "rsg_grad_tol", "ss", "ss_fixed", "ss_moving",
  "threading", "thresh_mean_intensity", "translation_scale_factor",
  ]
  # loop through the stage parameters and create the command for each stage
  final_stage_params_list = []
  for stage_params in stage_params_list:
    final_stage_params = defaultdict(str)
    for key in stage_params:
      if key in stage_param_possible_key_list:
        final_stage_params[key] = stage_params[key]
    final_stage_params_list.append(final_stage_params) 

  # create the parm.txt file in the same directory as image_out
  out_dir = Path(final_global_params["image_out"]).parent
  os.makedirs(out_dir, exist_ok=True)
  parm_txt_path = out_dir.joinpath("parm.txt")
  param_txt = "[Global]\n"
  for key in final_global_params:
    param_txt += f"{key}={final_global_params[key]}\n"
  param_txt += "\n"
  for stage in final_stage_params_list:
    param_txt += "[Stage]\n"
    for key in stage:
      param_txt += f"{key}={stage[key]}\n"
    param_txt += "\n"

  with open(parm_txt_path, "w") as f:
    f.write(param_txt)
  
  command = ["plastimatch", "register", str(parm_txt_path)]
  try:
    registration_summary = subprocess.run(command, capture_output = True, check = True)
  except Exception as e:
    print(e)
