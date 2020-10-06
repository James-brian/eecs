import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt,style
from scipy.stats import binom 

import math
import mpld3
import PIL

import numpy as np


from threading import RLock

import random
from collections import Counter

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure 
import io

verrou = RLock() 

plt.style.use('dark_background')

                
def converter(message):
    num = message.split(',')
    l = list(map(float,num))
    return l

#normal_distribution
def	normal_pdf(x,mu=0,sigma=1):
	sqrt_two_pi	= math.sqrt(2 * math.pi)				
	return (math.exp(-(x-mu) ** 2 / (2 * sigma ** 2)) / (sqrt_two_pi * sigma))


def	normal_cdf(x,mu=0,sigma=1):	
	
	return (1 + math.erf((x - mu) / (math.sqrt(2) * sigma))) / 2


