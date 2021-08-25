"""
    ----------------------------------------
    PyPlastimatch
    
    Data utility functions
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""


import os
import numpy as np
import SimpleITK as sitk


def save_binary_segmask(path_to_header_file, path_to_output, pred_binary_segmask):
    
    """
    blabla
    
    Args:
        path_to_header_file: path to the NRRD file to be read with SITK in order to copy the 
                             header information from it
        path_to_output: location where to save the binary segmask (in one of the ITK supported formats)
        pred_binary_segmask: numpy array storing the binary segmask to save
    """
    
    sitk_copy_header = sitk.ReadImage(path_to_header_file)
    
    sitk_pred_binary = sitk.GetImageFromArray(pred_binary_segmask)
    sitk_pred_binary.CopyInformation(sitk_copy_header)
    sitk.WriteImage(sitk_pred_binary, path_to_output)
