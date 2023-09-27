"""
    ----------------------------------------
    PyPlastimatch
    
    Viz tools for notebook testing
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dbontempi@bwh.harvard.edu
    ----------------------------------------
    
"""

import numpy as np
import ipywidgets as ipyw
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

class AxialSliceFigure:
  """ 
  Base class for the interactive slice-wise visualisation widgets
  
  Init of all the figure parameters that are always set.

  @Params:
    ct_cmap - required : colormap for the CT viz. 
    figsize - required : size of the figure (in inches).
    dpi     - required : DPI of the figure.
    min_hu  - required : minimum HU to be visualised
    max_hu  - required : maximum HU to be visualised
  """
  
  def __init__(self, ct_cmap, figsize, dpi, min_hu, max_hu):

    self.ct_cmap = ct_cmap
    self.figsize = figsize
    self.dpi = dpi

    self.min_hu = min_hu
    self.max_hu = max_hu


  def views(self):
    """ 
    method description goes here
    
    """

    ipyw.interact(self.plot_slice, 
                  axial_idx = ipyw.IntSlider(min = 0, max = self.max_axial,
                                             step = 1, continuous_update = True,
                                             description = 'Axial slice:'))

## ----------------------------------------
## ----------------------------------------

class AxialSliceComparison(AxialSliceFigure):
  """ 
  class description goes here
  
  """
  
  def __init__(self, ct_volume_left, ct_volume_right,
               title_left = "", title_right = "",
               ct_cmap = "gray", figsize = (12, 12), dpi = 100,
               min_hu = -1024, max_hu = 3072):
    
    super().__init__(ct_cmap, figsize, dpi, min_hu, max_hu)

    # the only constraint should be on the number of axial slice of the volumes to visualise
    assert ct_volume_left.shape[0] == ct_volume_right.shape[0]

    self.ct_volume_left = ct_volume_left
    self.ct_volume_right = ct_volume_right
    self.max_axial = self.ct_volume_left.shape[0] - 1
   
    self.title_left = title_left
    self.title_right = title_right

    ipyw.interact(self.views)
  

  def plot_slice(self, axial_idx):
    """ 
    method description goes here
    
    """

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize = self.figsize, dpi = self.dpi)

    # plot CT axial slices
    ax_left.set_title(self.title_left)
    ax_left.imshow(self.ct_volume_left[axial_idx, :, :], cmap = self.ct_cmap,
                   vmin = self.min_hu, vmax = self.max_hu)
    
    ax_right.set_title(self.title_right)
    ax_right.imshow(self.ct_volume_right[axial_idx, :, :], cmap = self.ct_cmap,
                    vmin = self.min_hu, vmax = self.max_hu)

    plt.subplots_adjust(hspace = 0.2)
    plt.show()
  

## ----------------------------------------
## ----------------------------------------

class AxialSliceSegmaskComparison(AxialSliceFigure):
  """ 
  class description goes here
  
  """
  
  def __init__(self, ct_volume, segmask_ai_dict, segmask_manual_dict,
               segmask_cmap_dict, segmask_alpha = 0.6, title_left = "", title_right = "",
               ct_cmap = "gray", figsize = (12, 12), dpi = 100,
               min_hu = -1024, max_hu = 3072):
    
    super().__init__(ct_cmap, figsize, dpi, min_hu, max_hu)

    self.ct_volume = ct_volume
    self.max_axial = self.ct_volume.shape[0] - 1

    self.segmask_ai_dict = segmask_ai_dict
    self.segmask_manual_dict = segmask_manual_dict

    self.segmask_cmap_dict = segmask_cmap_dict
    self.segmask_alpha = segmask_alpha
    
    self.title_left = title_left
    self.title_right = title_right

    ipyw.interact(self.views)


  def plot_slice(self, axial_idx):
    """
    method description goes here
    
    """

    fig, (ax_ai, ax_manual) = plt.subplots(1, 2, figsize = self.figsize, dpi = self.dpi)

    # plot CT axial slices
    ax_ai.set_title(self.title_left)
    ax_ai.imshow(self.ct_volume[axial_idx, :, :], cmap = self.ct_cmap,
                 vmin = self.min_hu, vmax = self.max_hu)
    
    ax_manual.set_title(self.title_right)
    ax_manual.imshow(self.ct_volume[axial_idx, :, :], cmap = self.ct_cmap,
                     vmin = self.min_hu, vmax = self.max_hu)

    # check the lenght of cmaps is enough to colour all the structures
    assert len(self.segmask_cmap_dict) == np.max([len(self.segmask_ai_dict),
                                                  len(self.segmask_manual_dict)])
    
    # plot overlaying masks
    for key in self.segmask_ai_dict:
      segmask_ai = self.segmask_ai_dict[key]
      segmask_cmap = self.segmask_cmap_dict[key]
      ax_ai.imshow(segmask_ai[axial_idx, :, :], label = key,
                   cmap = segmask_cmap, alpha = self.segmask_alpha)

    for key in self.segmask_manual_dict:
      segmask_manual = self.segmask_manual_dict[key]
      segmask_cmap = self.segmask_cmap_dict[key]
      ax_manual.imshow(segmask_manual[axial_idx, :, :], label = key,
                       cmap = segmask_cmap, alpha = self.segmask_alpha)

    plt.subplots_adjust(hspace = 0.2)
    plt.show()

## ----------------------------------------
## ----------------------------------------

class AxialSliceSegmaskViz(AxialSliceFigure):
  """ 
  class description goes here
  
  """
  
  def __init__(self, ct_volume, segmask_dict, segmask_cmap_dict,
               segmask_alpha = 0.4,
               random_cmap = False, # FIXME - legend in the figure is wrong
               fig_title = "",
               ct_cmap = "gray", figsize = (6, 6), dpi = 100,
               min_hu = -1024, max_hu = 3072):
    
    """ 
    constructor description goes here
    
    """
    
    super().__init__(ct_cmap, figsize, dpi, min_hu, max_hu)

    self.ct_volume = ct_volume
    self.max_axial = self.ct_volume.shape[0] - 1

    self.segmask_dict = segmask_dict

    self.fig_title = fig_title
    
    if random_cmap:
      self.segmask_cmap_dict = self.get_random_cmap_dict(segmask_dict.keys())
    else:
      self.segmask_cmap_dict = segmask_cmap_dict

    self.segmask_alpha = segmask_alpha
    
    ipyw.interact(self.views)
  

  def get_random_cmap_dict(self, dict_keys):
    """ 
    method description goes here
    
    """

    segmask_cmap_dict = dict()

    for idx, key in enumerate(dict_keys):
      # dummy random colormap creation
      vals = np.linspace(0, 1, 256)
      np.random.shuffle(vals)

      # color map to sample from
      my_cmap = plt.cm.jet(vals)
      my_cmap[:, -1] = np.linspace(0, 1, 256)

      segmask_cmap_dict[key] = ListedColormap(my_cmap)

    return segmask_cmap_dict


  def plot_slice(self, axial_idx):
    """
    method description goes here
    
    """

    fig, ax = plt.subplots(1, 1, figsize = self.figsize, dpi = self.dpi)

    try:
      len(legend_elements)
    except:
      legend_elements = list()

    # plot CT axial slices
    ax.set_title(self.fig_title)
    ax.imshow(self.ct_volume[axial_idx, :, :], cmap = self.ct_cmap,
              vmin = self.min_hu, vmax = self.max_hu)

    # check the lenght of cmaps is enough to colour all the structures
    assert len(self.segmask_cmap_dict) == len(self.segmask_dict)
    
    # plot overlaying masks
    for key in self.segmask_dict:
      segmask = self.segmask_dict[key]
      segmask_cmap = self.segmask_cmap_dict[key]

      ax.imshow(segmask[axial_idx, :, :], label = key,
                cmap = segmask_cmap, alpha = self.segmask_alpha)
      
      if not len(legend_elements) == len(self.segmask_dict):        
        legend_elements.append(Patch(facecolor = segmask_cmap(0.7),
                                     edgecolor = 'k',
                                     label = key))
      
    plt.subplots_adjust(hspace = 0.2)
    plt.show()

    ax.legend(handles = legend_elements,
              loc = 'upper left',
              bbox_to_anchor = (1, 1))
