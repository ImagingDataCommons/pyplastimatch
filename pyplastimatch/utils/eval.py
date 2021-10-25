"""
    ----------------------------------------
    PyPlastimatch
    
    Eval utility functions
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""

import os
import json
import numpy as np
import pandas as pd

def dc_dict_to_df(dc_dict, structure_name):
    
    """
    Format the Dice Coefficient results dictionary to a more human-readable Dataframe.
    
    Args:
      dc_dict: dictionary containing the results information.
        The dictionary should be formatted like the following (eval script output):
        
        {'LUNG1-002': {'heart': {'com': {'ref': [35.0662, -47.6561, -34.145],
                                         'cmp': [35.0477, -49.1853, -34.787]},
                                 'dc': 0.939273},
                      'esophagus': {'com': {'ref': [10.0202, -1.10146, 29.832],
                                            'cmp': [7.15864, 2.45604, 34.21]},
                                    'dc': 0.745591}},
        ...
        }
        
      structure_name: name of the structure the Dataframe should be about (e.g., "heart")
      
    """
    
    df_dict = dict()

    for pat in dc_dict.keys():
        pat_dict = dc_dict[pat][structure_name]

        tmp = dict()
        
        try:
            tmp["com_ref_x0"], tmp["com_ref_x1"], tmp["com_ref_x2"] = pat_dict["com"]["ref"]
            tmp["com_cmp_x0"], tmp["com_cmp_x1"], tmp["com_cmp_x2"] = pat_dict["com"]["cmp"]
            tmp["dc"] = pat_dict["dc"]
        except:
            tmp["com_ref_x0"], tmp["com_ref_x1"], tmp["com_ref_x2"] = np.full([3], np.nan).tolist()
            tmp["com_cmp_x0"], tmp["com_cmp_x1"], tmp["com_cmp_x2"] = np.full([3], np.nan).tolist()
            tmp["dc"] = np.nan
        
        df_dict[pat] = tmp
        
    return pd.DataFrame.from_dict(df_dict, orient = "index")
    
## ----------------------------------------

def hd_dict_to_df(hd_dict, structure_name):
    
    """
    Format the Hausdorff Distance results dictionary to a more human-readable Dataframe.

    
    Args:
      hd_dict: dictionary containing the results information.
        The dictionary should be formatted like the following (eval script output):
        
        {'LUNG1-002': {'heart': {'hd': 8.999999,
                                 'hd95': 1.5,
                                 'hd_boundaries': 8.999999,
                                 'hd95_boundaries': 7.373553},
                       'esophagus': {'hd': 31.477112,
                                     'hd95': 8.945594,
                                     'hd_boundaries': 31.477112,
                                     'hd95_boundaries': 12.433664}},
        ...
        }
        
      structure_name: name of the structure the Dataframe should be about (e.g., "heart")
      
    """
      
    df_dict = dict()

    for pat in hd_dict.keys():
        pat_dict = hd_dict[pat][structure_name]

        tmp = dict()
        
        for key in pat_dict.keys():
            try:
                tmp[key] = pat_dict[key]
            except:
                tmp[key] = np.nan
        
        df_dict[pat] = tmp
        
    return pd.DataFrame.from_dict(df_dict, orient = "index")
  
## ----------------------------------------

