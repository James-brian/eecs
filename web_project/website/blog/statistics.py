from __future__ import division
from collections import Counter
import math
import numpy as np

#dataA = [360,320,310,300,240,280,250,220,200,180,160,140,120,100,80,75,70,60,55,50,45,40,35,30,33,25,25,22,22,20,20,19,19,18,17,16,16,16,16,15,15,15,15,14,13,10,8,5,2,2]
#dataB = [100,49,41,40,40,40,25,22,22,20,20,19,19,17,16,16,16,16,15,13,12,11,11,10,10,9,9,9,8,8,7,7,6,6,5,5,4,4,3,2,2,2,2,2,1,1,1,1,1,1]

def converter(message):
    num = message.split(' ')
    l = list(map(int,num))
    return l

#message = input('input a number:') 


class CentralTendency:

	def __init__(self,x):
		self.x = x
		
	def mean(self):
		mean_n = sum(self.x)/len(self.x)
		return mean_n

	def median(self):

		n = len(self.x)
		sorted_v = sorted(self.x)
		midpoint = n//2 #indices  must be integers not float so we avoid (n/2)
		if n%2 == 1:
			#if odd 
			return sorted_v[midpoint]

		else:
			#if even
			lowpoint = midpoint - 1
			highpoint = midpoint
			return (sorted_v[lowpoint] + sorted_v[highpoint])/2

	def mode(self):

		count_items = Counter(self.x)
		max_count = max(count_items.values())

		return [x_i for x_i,count in count_items.items() if count == max_count]


class Dispersion:

	def __init__(self,x,p=0.75,q=0.25):
		self.x = x
		self.p = p
		self.q = q
		

	def mean(self):
		mean_n = sum(self.x)/len(self.x)
		return mean_n

	def sqr_deviation(self,m):
		return [(m_i - self.mean())**2 for m_i in m]

	def deviation(self,z):
		return [(z_i - self.mean()) for z_i in z]


	def quantile(self,o):
		index = int(o*len(self.x))
		sorted_value = sorted(self.x)
		return sorted_value[index]

	def variance(self,f):
		n = len(self.x)
		dev = self.sqr_deviation(f)
		return (sum(dev)/(n-1))

	def standard_deviation(self,g):
		variance = self.variance(g)
		return math.sqrt(variance)

	def interquartile_range(self):
		return (self.quantile(self.p) - self.quantile(self.q))

#d = Dispersion(dataB,dataA,p = 0.75,q =0.25)
    
#d = Dispersion(emoji_converter(message))

#print(d.covariance(dataB,dataA))
#print(d.mean())


class Correlation:

	def __init__(self,x,y,p=0.75,q=0.25):
		self.x = x
		self.p = p
		self.q = q
		self.y = y
		

	def mean(self):
		mean_n = sum(self.x)/len(self.x)
		return mean_n

	def sqr_deviation(self,m):
		return [(m_i - self.mean())**2 for m_i in m]

	def deviation(self,z):
		return [(z_i - self.mean()) for z_i in z]


	def quantile(self,o):
		index = int(o*len(self.x))
		sorted_value = sorted(self.x)
		return sorted_value[index]

	def variance(self,f):
		n = len(self.x)
		dev = self.sqr_deviation(f)
		return (sum(dev)/(n-1))

	def standard_deviation(self,g):
		variance = self.variance(g)
		return math.sqrt(variance)

	def interquartile_range(self):
		return (self.quantile(self.p) - self.quantile(self.q))

	def covariance(self,a,b):
		n = len(self.x)
		return np.dot(self.deviation(a),self.deviation(b))/n-1 #sample variance

	def correlation(self):  
		"""
		std_dev_x = self.standard_deviation(self.x) 
		std_dev_y = self.standard_deviation(self.y)
		if std_dev_x > 0 and std_dev_y > 0:
			return (self.covariance(self.x,self.y)/np.dot((std_dev_x),(std_dev_y)))
		else:
			return 0
		"""
		#or you can do this
		var_x = self.variance(self.x)
		var_y = self.variance(self.y)
		if var_x > 0 and var_y >0 :
			return (self.covariance(self.x,self.y))/math.sqrt(np.dot(var_x,var_y))
		else:
			return 0