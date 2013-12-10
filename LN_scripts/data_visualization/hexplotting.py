#!/usr/bin/env python
# encoding: utf-8
"""
CCAW.py

Created by McKell Carter on 2012-03-22.
Modified by Lawrence Ngo throughout 2012. 
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/") # This allows for the appropriate import of matplotlib on Law's mac.
import os
import unittest
import numpy as N
import nibabel # Pynifti is no longer supported, and it is not supported under the NiBabel package.
import scipy.odr
import matplotlib as mpl
mpl.use('Agg')
import pylab as plt
import matplotlib.cm as cm
import matplotlib.path as path
from matplotlib import patches
from matplotlib import collections
from matplotlib import pyplot
from matplotlib.patches import Ellipse
from scipy import stats
from matplotlib.font_manager import FontProperties


## CCAW - Cognitive Contrast Analyzer Whole-brain

# BaseData can be either three dimensional of four dimensional.
class BaseData:
	def __init__(self, image_pname, mask_pname): 
		self.image_pname = image_pname
		self.mask_pname = mask_pname
		self.image = nibabel.load(self.image_pname)
		self.image_data = self.image.get_data()
		self.mask = nibabel.load(self.mask_pname)
		self.mask_data = self.mask.get_data() > 0
		print('Dimensions of the image are '+str(self.image_data.shape))
		print('Dimensions of the mask are '+str(self.mask_data.shape))
		if (self.image_data.ndim==3) & (self.mask_data.ndim==3):
			self.masker()
			 
	def masker(self):
		if self.image_data.shape==self.mask_data.shape:
			self.image_data_masked = self.image_data[self.mask_data]
		else:
			print('The dimensions of the image and the mask are not the same!')
			sys.exit()

class Analysis3D:
	def __init__(self, x, y, out_pname):
		self.x = x
		self.y = y
		# If x and y are both three dimensional arrays, then run the following.
		self.run_linear_odr_on_subj_mean(x, y)
		#self.plot_ellipse(self.x.image_data_masked, self.y.image_data_masked)
		self.plot_subj_mean(x, y, out_pname)

	#odr fit and plot residuals
	def f(self, B, x):
		return B[0]*x + B[1]

	# Inputs should be masked 3D numpy arrays. 
	def run_linear_odr_on_subj_mean(self, x, y, slope0=0., intercept0=0., expected_x=0., expected_y=0.):
		linear = scipy.odr.Model(self.f)  #make model object from the eq above
		odr_data = scipy.odr.RealData(x.reshape(-1)-expected_x, y.reshape(-1)-expected_y)  #data must be a single dimension (flat) - this is what reshape(-1) does   
		self.odr_model = scipy.odr.odrpack.ODR(odr_data, linear, beta0=[slope0,intercept0])
		self.odr_out =  self.odr_model.run()
		self.odr_slope, self.odr_intercept = self.odr_out.beta    #slope and intercept values from odr output
		self.odr_predY = self.odr_slope*x.reshape(-1) + self.odr_intercept
		self.odr_predX = (1./self.odr_slope)*y.reshape(-1) - (self.odr_intercept/self.odr_slope)
		
	def plot_ellipse(self, x, y, nstd=2, ax=None, **kwargs):
		x = x.reshape(-1)
		y = y.reshape(-1)
		xtransposed = N.expand_dims(x,axis=1)
		ytransposed = N.expand_dims(y,axis=1)
		allpoints = N.concatenate((xtransposed,ytransposed), axis=1)
		center = allpoints.mean(axis=0)
		covariance = N.cov(allpoints, rowvar=False)
		
		def eigsorted(covariance):
			vals, vecs = N.linalg.eig(covariance)
			order = vals.argsort()[::-1]
			return vals[order], vecs[:,order]
				
		
		vals, vecs = eigsorted(covariance)
		theta = N.degrees(N.arctan2(*vecs[:,0][::-1]))
		width, height = 2 * nstd * N.sqrt(vals)
		self.flattening = (width-height)/width
		self.ellip = Ellipse(xy=center, width=width, height=height, angle=theta, **kwargs)
		
	# Again, inuts should be masked 3D numpy arrays.	
	def plot_subj_mean(self, x, y, out_fname='', density_cmap=cm.spectral_r, density_alpha=0.5):
		self.fig = plt.figure(figsize=(3., 3.), dpi=150.)     
		self.ax = self.fig.add_axes([0.1, 0.125, 0.75, 0.75])#, axisbg='w') 
		self.ax_cb = self.fig.add_axes([0.87, 0.15, 0.025, 0.72])
		self.ax.xaxis.set_ticks_position('bottom')
		self.ax.yaxis.set_ticks_position('left')
		# this_max = N.max(N.array(N.max(x.reshape(-1)), N.max(y.reshape(-1))))
		this_min = -1 
		this_max = 1
		self.ax.plot(N.arange(this_min,this_max), N.arange(this_min,this_max), 'b:')    #add 1 to 1 line
		self.ax.plot(N.arange(this_min,this_max), self.odr_slope*N.arange(this_min,this_max)+self.odr_intercept, 'g--', lw=1.5, alpha=0.9) #plot regression
		self.ax.plot(N.arange(this_min,this_max), N.zeros(len(N.arange(this_min,this_max))), 'k--', lw=0.5, alpha=0.9)    #add y = 0
		self.ax.plot(N.zeros(len(N.arange(this_min,this_max))), N.arange(this_min,this_max), 'k--', lw=0.5, alpha=0.9)    #add x = 0
		
	    #plot 2d-density
		cmap_min = 1.  #cmap_min = N.min(sorted_map_improve_array)
		cmap_max = 100.   #cmap_max = N.max(sorted_map_improve_array)
		cmap_range = cmap_max - cmap_min
		cmap_norm = mpl.colors.Normalize(vmin=cmap_min, vmax=cmap_max)
		cmap =  density_cmap #cm.spectral_r
		
		self.ax.hexbin(x.reshape(-1), y.reshape(-1), norm=cmap_norm, cmap=density_cmap, alpha=density_alpha, mincnt=1)   #vmin=1, vmax=100,
		#self.ax.add_artist(self.ellip)
		self.cb = mpl.colorbar.ColorbarBase(self.ax_cb, cmap=cmap, norm=cmap_norm, orientation='vertical')
		    
		#odr_txt_summary = 'odr slope: %.3f, se: %.3f \nodr intercept: %.3f, se: %.3f \nflattening: %.3f'  % (self.odr_slope, self.odr_out.sd_beta[0], self.odr_intercept, self.odr_out.sd_beta[1], self.flattening)
		odr_fp = FontProperties(family='Arial', weight='normal', size=8)   #tick properties
		#self.fig.text(0.3, 0.2, odr_txt_summary, fontproperties=odr_fp) #write ODR summary 		
		
		if len(out_fname)>0:
			self.fig.savefig(out_fname, dpi=300)
			print("Results have been printed to "+ out_fname)
		else:
			self.fig.show()
			

			

    	
	