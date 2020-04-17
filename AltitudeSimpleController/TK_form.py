#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: MKargus0

"""
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import Altitude_Control as Ati
import numpy as np




class MainWindow(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.wm_title(self,"Simulator")
        container=tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames={}
        for F in (StartPage,ResultPage):
            frame =F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(StartPage)
        
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

        
droneList = [None]
LARGE_FONT=("verdana",12)
axesList = []

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Parameters",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        
        button1=ttk.Button(self,text="Result",
                           command=lambda:controller.show_frame(ResultPage))
        button1.pack()
        
        label_t0=tk.Label(self,text="t0 - start time")
        label_t0.pack()
        self.timeStart_entery = tk.Entry(self)
        self.timeStart_entery.insert(tk.END, '0')
        self.timeStart_entery.pack()
        
        label_tT=tk.Label(self,text="T - total time")
        label_tT.pack()
        self.totalTime_entery = tk.Entry(self)
        self.totalTime_entery.insert(tk.END, '10')
        self.totalTime_entery.pack()
        
        label_dt=tk.Label(self,text="dt - model step")
        label_dt.pack()
        self.dt_entery = tk.Entry(self)
        self.dt_entery.insert(tk.END, '0.1')
        self.dt_entery.pack()
        
        label_mass=tk.Label(self,text="UAV mass(kg)")
        label_mass.pack()
        self.mass_entery = tk.Entry(self)
        self.mass_entery.insert(tk.END, '0.7')
        self.mass_entery.pack()
        
        label_mT=tk.Label(self,text="UAV max trust(Newton)")
        label_mT.pack()
        self.mT_entery = tk.Entry(self)
        self.mT_entery.insert(tk.END, '12')
        self.mT_entery.pack()
        
        label_minT=tk.Label(self,text="UAV min trust(Newton)")
        label_minT.pack()
        self.minT_entery = tk.Entry(self)
        self.minT_entery.insert(tk.END, '0.3')
        self.minT_entery.pack()
        
        label_PID=tk.Label(self,text="PID controller settings",font=LARGE_FONT)
        label_PID.pack()
        
        label_Kp=tk.Label(self,text="Kp")
        label_Kp.pack()
        self.Kp_entery = tk.Entry(self)
        self.Kp_entery.insert(tk.END, '25')
        self.Kp_entery.pack()
        
        label_Ki=tk.Label(self,text="Ki")
        label_Ki.pack()
        self.Ki_entery = tk.Entry(self)
        self.Ki_entery.insert(tk.END, '0')
        self.Ki_entery.pack()
        
        label_Kd=tk.Label(self,text="Kd")
        label_Kd.pack()
        self.Kd_entery = tk.Entry(self)
        self.Kd_entery.insert(tk.END, '3')
        self.Kd_entery.pack()
        
        self.FeedForward = tk.BooleanVar()
        self.FeedForward.set(0)
        
        FF_checkbtn = tk.Checkbutton(text="FeedForward",
                                            variable=self.FeedForward,
                                            onvalue=1, offvalue=0)
        FF_checkbtn.pack()
        
        self.external_influence = tk.BooleanVar()
        self.external_influence.set(0)
        
        external_influence_checkbtn = tk.Checkbutton(text="external influence",
                                            variable=self.external_influence,
                                            onvalue=1, offvalue=0)
        external_influence_checkbtn.pack()
        
        
        droneCreateButton=ttk.Button(self,text="add",command=self.addDrone)
        droneCreateButton.pack()
        
        label_setPoint=tk.Label(self,text="Setpoint position settings",font=LARGE_FONT)
        label_setPoint.pack()
        
        label_desPose=tk.Label(self,text="desire Position")
        label_desPose.pack()
        self.desPose_entery = tk.Entry(self)
        self.desPose_entery.insert(tk.END, '10')
        self.desPose_entery.pack()
        
        label_desPoseTime=tk.Label(self,text="setpoint time start")
        label_desPoseTime.pack()
        self.desPoseTime_entery = tk.Entry(self)
        self.desPoseTime_entery.insert(tk.END, '3')
        self.desPoseTime_entery.pack()
        
        
        addSetpoint_button=ttk.Button(self,text="addSetpoint",
                           command=self.addSetpoint)
        addSetpoint_button.pack()
        
        
        
        #self.
    def addDrone(self):
        
        mass = float(self.mass_entery.get())
        maxTrust = float(self.mT_entery.get())
        t0 = float(self.timeStart_entery.get())
        totalTime = float(self.totalTime_entery.get())
        dt = float(self.dt_entery.get())
        kp = float(self.Kp_entery.get())
        ki = float(self.Ki_entery.get())
        kd = float(self.Kp_entery.get())
        minLimit = float(self.minT_entery.get())
        
        drone = Ati.multicopter(mass,maxTrust,0,t0,totalTime,dt,self.external_influence.get(),
                                self.FeedForward.get())
        drone.kp = kp
        drone.kd = kd
        drone.ki = ki
        drone.acc_minLimit = minLimit/mass
        
       
        
        droneList[0]=drone
        
        print('drone added')
    
    def addSetpoint(self):
        if droneList[0] != None:
            droneList[0].setpointList.append([float(float(self.desPose_entery.get()),
                                                    self.desPoseTime_entery.get())])
    
        
class ResultPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Result",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button=ttk.Button(self,text="Parameters",
                          command=lambda: controller.show_frame(StartPage))
        button.pack()
        
        clear_button=ttk.Button(self,text="Clear",
                          command=self.clearPlots)
        clear_button.pack()
        
        
        
        self.dynamic_scale = tk.BooleanVar()
        self.dynamic_scale.set(0)
        
        dyn_scale_checkbtn = tk.Checkbutton(text="plot autoscale",
                                            variable=self.dynamic_scale,
                                            onvalue=1, offvalue=0)
        dyn_scale_checkbtn.pack()
    
        
        self.plotList = []
        f=Figure(figsize=(5,5),dpi=100)
        spec = gridspec.GridSpec(ncols=1, nrows=3, figure=f)
        plotPose = f.add_subplot(spec[0, 0])
        plotVel = f.add_subplot(spec[1, 0])
        plotAcc = f.add_subplot(spec[2, 0])
        plotPose.grid(True)
        plotVel.grid(True)
        plotAcc.grid(True)
        canvas = FigureCanvasTkAgg(f,self)
        plotPose.set_ylabel("Position")
        plotVel.set_ylabel("velocity")
        plotAcc.set_ylabel("Acceleration")
        plotAcc.set_xlabel("Time")
        
        '''set x and y axes limit for plot's'''
        plotPose.set_xlim(-1,30)
        plotPose.set_ylim(-20,20)
        plotVel.set_xlim(-1,30)
        plotVel.set_ylim(-20,20)
        plotAcc.set_xlim(-1,30)
        plotAcc.set_ylim(-20,20)
        
        axPose, = plotPose.plot([],[],'r-')
        axVel, = plotVel.plot([],[],'g-')
        axAcc, = plotAcc.plot([],[],'b-')
        
        self.plotList.append(plotPose)
        self.plotList.append(plotVel)
        self.plotList.append(plotAcc)
        #self.canvas = canvas
        
        '''add axes'''
        axesList.append(axPose)
        axesList.append(axVel)
        axesList.append(axAcc)
        '''add canvas'''
        axesList.append(canvas)
        
        StartButton=ttk.Button(self,text="Start simulation",
                               command=self.StartSimulation)
        StartButton.pack()
        #b.scatter(t,F,color='red')
        #b.plot(t,F,t,G)
        #b.grid(True)
        #b.set_xscale('log')
        #Figure.add_gridspec(self,1,1)
        canvas.draw()
        
        canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
        
        
        toolbar=NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        
    def StartSimulation(self):
            print("work")
            print('ok',droneList)
                    
            '''add new data on plot'''
            def plotUpdate(stateVector,time):
                for i in range(len(axesList)-1):
                    axesList[i].set_xdata(np.append(axesList[i].get_xdata(),time))
                    axesList[i].set_ydata(np.append(axesList[i].get_ydata(),stateVector[i]))
                    if self.dynamic_scale.get() == True:
                            self.plotList[i].set_xlim(time-5,time+0.5)
                            self.plotList[i].set_ylim(stateVector[i]-10,stateVector[i]+10)
                    else:
                        pass
            
            
            while droneList[0].time <= droneList[0].totalTime:
                    stateVector,time = droneList[0].altitudeControlStep()
                    print('----------------------------')
                    print(stateVector)
                    print(time)
                    print('----------------------------')
                    
                   
                    plotUpdate(stateVector,time)
                    
                    '''last plotlist element is canvas'''
                    axesList[3].draw()
            
            droneList.clear()
            droneList.append(None)
            print('simulation end')  
        
            
    def clearPlots(self):
        for i in range(len(self.plotList)):
            self.plotList[i].cla()
            self.plotList[i].grid()
            self.plotList[i].set_xlim(-1,30)
            self.plotList[i].set_ylim(-20,20)
        
        self.plotList[0].set_ylabel("Position")
        self.plotList[1].set_ylabel("velocity")
        self.plotList[2].set_ylabel("Acceleration")
        self.plotList[2].set_xlabel("Time")
        axesList[3].draw()
        axesList[0], = self.plotList[0].plot([],[],'r-')
        axesList[1], = self.plotList[1].plot([],[],'g-')
        axesList[2], = self.plotList[2].plot([],[],'b-')
       
        print('clear axes')
 
    
        
