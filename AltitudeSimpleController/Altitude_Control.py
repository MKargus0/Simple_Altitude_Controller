#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: MKargus0

"""
#from matplotlib import pyplot as plt
import numpy as np
#import time
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class multicopter:
    def __init__(self,m,T,z,t0,totalTime,dt,use_external_influence,use_Feed_forward):
        self.mass = m
        self.g = 9.8066
        self.maxTrust = T
        self.pos = z
        self.vel = 0
        self.acc = 0
        self.desPos = 0
        self.desVel = 0
        self.desAcc = 0
        '''we use lastDesPose and lastDesVel to calculate feed forwarding'''
        self.lastDesPos = 0
        self.lastDesVel = 0
        self.desPostime = 2
        self.posData = []
        
        self.stateVector = [self.pos,self.vel,self.acc]
        
        
        self.time = t0
        self.totalTime =totalTime
        self.t0 = t0
        self.dt = dt
        
        self.acc_maxLimit = T/self.mass
        self.acc_minLimit = 0
        
        self.u = 0
        self.error =0
        self.lasterror = 0
        
        self.use_external_influence = use_external_influence
        self.use_Feed_forward = use_Feed_forward
        self.kp = 25
        self.kd = 3
        self.ki = 0
        self.I = 0
        self.setpointList = []
  
        
    def altitudeControlStep(self):       
        
            '''Check for new setpoint's'''
            if self.time >= self.desPostime:
                self.desPos = 10
            """Do system model step """
            self.doStep()
            '''use saturation for limit our contol function value'''
            self.acc = self.saturation(self.u) -self.g
            print(self.use_external_influence)
            if self.use_external_influence == True:
                self.acc += np.random.normal(2,3)
                print('stohasticka eee')
            print('acc',self.acc)
            self.vel += self.acc * self.dt
            self.pos += self.vel * self.dt
            if self.pos < 0:
                self.pos = 0
                self.acc = 0
                self.vel = 0
            '''add data to state vector'''
            self.stateVector = [self.pos,self.vel,self.acc]
            self.time += self.dt
            
            print(self.time)
            #input()
            return self.stateVector,self.time
    
    def doStep(self):
        
        '''get error function value'''
        self.error = self.desPos - self.pos
        '''get Proportional value '''
        P = self.kp * self.error
        '''get Integral value '''
        self.I += self.ki * self.error * self.dt
        '''get Derivative value '''
        D = self.kd * ((self.error-self.lasterror)/self.dt)
        
        '''get FeedForward value '''
        if self.use_Feed_forward == True:
            self.desVel = ((self.desPos-self.lastDesPos)/self.dt)
            FF = ((self.desVel-self.lastDesVel)/self.dt)
        else:
            FF = 0
        print('FF--',FF)
        '''get control function value '''
        self.u = P + self.I + D 
        print('u= ',self.u)
        '''set last error value for using in the future step's'''
        self.lasterror = self.error
        self.lastDesPos = self.desPos
        self.lastDesVel = self.desVel
     
    def saturation(self,u):
        
        if u > self.acc_maxLimit:
            u = self.acc_maxLimit
        if u < self.acc_minLimit:
            u = self.acc_minLimit
        else :
            pass
        return u

   

#m1 = multicopter(1,30,0)
#m1.drawPlot()  
#m1.altitudeControl()   