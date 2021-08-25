"""
    ----------------------------------------
    PyPlastimatch
    
    Viz tools for notebook testing
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""

import numpy as np
import ipywidgets as ipyw
import matplotlib.pyplot as plt


class AxialSliceSegmaskComparison:
  """ 
  description goes here
  
  """
  
  def __init__(self, ct_volume, segmask_ai_dict, segmask_manual_dict,
               segmask_cmap_dict, segmask_alpha = 0.6, ct_cmap = "gray",
               figsize = (12, 12), dpi = 100):
    
    self.ct_volume = ct_volume
    
    self.segmask_ai_dict = segmask_ai_dict
    self.segmask_manual_dict = segmask_manual_dict

    self.figsize = figsize
    self.dpi = dpi
    
    self.ct_cmap = ct_cmap
    self.segmask_cmap_dict = segmask_cmap_dict
    self.segmask_alpha = segmask_alpha
    
    self.v = [np.min(ct_volume), np.max(ct_volume)]

    # Call to select slice plane
    ipyw.interact(self.views)
  
  def views(self):
    max_axial = self.ct_volume.shape[0] - 1

    ipyw.interact(self.plot_slice, 
                  axial_idx = ipyw.IntSlider(min = 0, max = max_axial,
                                             step = 1, continuous_update = True,
                                             description = 'Axial slice:'), 
                  )

  def plot_slice(self, axial_idx):

    fig, (ax_ai, ax_manual) = plt.subplots(1, 2, figsize = self.figsize, dpi = self.dpi)

    # plot CT axial slices
    ax_ai.set_title("nnU-Net")
    ax_ai.imshow(self.ct_volume[axial_idx, :, :], cmap = self.ct_cmap, vmin = -1024, vmax = 1024)
    
    ax_manual.set_title("Manual")
    ax_manual.imshow(self.ct_volume[axial_idx, :, :], cmap = self.ct_cmap, vmin = -1024, vmax = 1024)

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

