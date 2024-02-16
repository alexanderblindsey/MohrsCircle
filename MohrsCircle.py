# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 21:14:25 2024

@author: alindsey

Taken in part from TopDogEngineer: https://www.youtube.com/watch?v=lRUkVG25bUU
"""

import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.patches import Arc # for angle
import math

class MohrsCircle():
        
    def __init__(self, sigmax, sigmay, tauxy):
        self.sigmax = sigmax
        self.sigmay = sigmay
        self.tauxy = tauxy      
        
    def circleCenter(self):
        c = (self.sigmax + self.sigmay) / 2
        return(c)
    

    def radius(self):
        """
        Pyhagorean theorem using sigmax to find radius
        """
        a = (self.sigmax - self.circleCenter()) ** 2
        b = (self.tauxy) ** 2
        c = math.sqrt(a + b)
        return(c)
    
    def maxPrincipleStressP(self):
        P = self.circleCenter() + self.radius()
        return(P)
    
    def minPrincipleStressQ(self):
        Q = self.circleCenter() - self.radius()
        return(Q)
    
    def maxShearStress(self):
        taumax = self.radius() * -1
        return taumax
    
    def minShearStress(self):
        taumin = self.radius()
        return taumin
    
    def principleStressAngle(self):
        try:
            
            inside = (2 * self.tauxy) / (self.sigmax - self.sigmay)
            theta1 = 0.5 * np.arctan(inside)
            
        except ZeroDivisionError:
            theta1 = 'Undefined'
            
        return theta1
    
    def get2Theta1(self):
        if self.principleStressAngle() == 'Undefined':
            doubletheta1 = 'Undefined'
        else:
            if self.principleStressAngle() < 0:
                doubletheta1 = (np.pi + self.principleStressAngle()) * 2
            else:
                doubletheta1 = self.principleStressAngle() * 2
        return doubletheta1

    # def buildArc(self, origin=[0,0], dims=1, angle=0):
    #     if 
                
        
    def plot(self, axisSize=14, titleSize=20):
        degrees = np.linspace(0, 360, 361) # creates array of whole numbers from 0-360
        radians = degrees * ((np.pi) / 180) # converts array to radians
        
        circle_xpoints = self.circleCenter() + self.radius() * np.cos(radians)
        circle_ypoints =  self.radius() * np.sin(radians)
    
        line_xpoints = (self.sigmax, self.sigmay)        
        if self.sigmax >= self.sigmay:
            line_ypoints = (self.tauxy, self.tauxy * -1)
        else:
            line_ypoints = (self.tauxy * -1, self.tauxy)
            
        xlabels = [self.maxPrincipleStressP(),
                   self.minPrincipleStressQ(),
                   self.circleCenter(),
                   self.circleCenter()]
        
        ylabels = [0, 0, self.maxShearStress(), self.minShearStress()]
        
        labels = ['P', 'Q', r'$\tau_{max}$', r'$\tau_{min}$']
        
        
        fig = plt.figure(figsize=[10,10])
        ax = fig.add_subplot()
        plt.gca().invert_yaxis()
        plt.title('Mohrs Circle', size=titleSize)
        plt.xlabel(r'$\sigma$', size=axisSize)
        plt.ylabel(r'$\tau$', size=axisSize)
        plt.grid()
        ax.plot(circle_xpoints, circle_ypoints,
                line_xpoints, line_ypoints, 'r')
        
        for x, y, l in zip(xlabels, ylabels, labels):
            ax.annotate(l, xy=(x, y), fontsize=axisSize)
            
        

x = MohrsCircle(0,0,-2500)
x.plot()

print('Center: (', x.circleCenter(), ', 0)')
print('Radius: ', x.radius())
print('P: ', x.maxPrincipleStressP(), ' psi')
print('Q: ', x.minPrincipleStressQ(),  ' psi')
print('Tau Max: ', x.maxShearStress())
print('Tau Min: ', x.minShearStress())

try:
    print('Theta_1: ', x.principleStressAngle() * (180 / np.pi))
    print('2 * Theta_1: ', x.get2Theta1() * (180 / np.pi))
except TypeError:
    print("Theta_1: Undefined \n2 * Theta_1: Undefined")
    
