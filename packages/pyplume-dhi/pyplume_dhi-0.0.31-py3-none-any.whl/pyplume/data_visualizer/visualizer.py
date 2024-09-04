# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:08:43 2022

@author: anba
"""

import pandas as pd
import numpy as np
import os,sys

from scipy.ndimage import gaussian_filter1d
import argparse
import matplotlib.cm as cm
import cmocean


import vispy 
from vispy.app import use_app, Timer
from vispy import app, visuals, scene
from vispy.io import imread, load_data_file, read_mesh, read_png
from vispy.visuals.transforms import STTransform,MatrixTransform
from vispy.io import read_mesh, load_data_file, imread
from vispy.scene.visuals import Mesh
from vispy.scene import transforms
from vispy.visuals.filters import ShadingFilter, WireframeFilter,TextureFilter


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import * 
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from scipy.ndimage import gaussian_filter1d

#%%
# from workhorse_adcp import workhorse_adcp as wh_adcp 
# from seabird_ctd import seabird_ctd as sb_ctd 

from ..ptools import ptools


import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd, numpy as np



#%%#############################################################################
#######################  INITIALIZE VISUALIZATION  ############################
###############################################################################
class PCV:
    def __init__(self):
        self.update_count = 0
        
    

        
    def init_plot(self,canvas):
        
        
        
        path = r'C:\Users\anba\OneDrive - DHI\Desktop\Visualization\PCV\PCV_Tracks_with_Time.csv'
        PCV_df = pd.read_csv(path, index_col = 0, parse_dates = True)
        PCV_df['z'].loc[PCV_df['z']>-4100] = np.mean(PCV_df['z'])
        PCV_df['z'] = PCV_df['z']
        PCV_df.drop(columns = 'id',inplace = True)
        PCV_df.dropna(inplace = True)
        
        pos = np.array([PCV_df['x'].tolist(),PCV_df['y'].tolist(),PCV_df['z'].tolist()]).T
        #PCV_carray = vispy.color.color_array.ColorArray(color=PCV_cmap(np.ones(len(PCV_df))), alpha=.1, clip=True, color_space='rgb')
        # scene.visuals.Line(pos =  self.adcp.geometry.position.T, width = .1, parent  = canvas.main_view.scene)

        self.PCV_tracks = scene.visuals.Markers(pos = pos, size = 1,parent =canvas.main_view.scene)     



        # self.ax = scene.visuals.XYZAxis(pos = self.adcp.geometry.position[:,0], parent=canvas.main_view.scene)
                                   
                                   

        
    def update(self):
        
        None

        
        
class IP_ROV:
    # y is the forward direction
    def __init__(self,name,adcp):
        # contains data 
        self.name = name # name of the asset 
        self.adcp = adcp
        
        self.platform_offset = np.array([-0.36,-1.45,-0.31]) # position of the center of the instrument platform (e.g., vessel) relative to the position measurement. 
        
        self.platform_width = 1.74
        self.platform_height = 2.74
       
        self.adcp_absolute_beam_midpoint_positions = adcp.geometry.get_absolute_beam_midpoint_positions()
        self.beam_data = adcp.get_ensemble_array(field_name = 'ABSOLUTE BACKSCATTER')
        
        
        self.timesteps = adcp.get_ensemble_datetimes()

    def init_plot(self,canvas):
        
        # scene.visuals.Line(pos =  self.adcp.geometry.position.T, width = .1, parent  = canvas.main_view.scene)
        
        
        
        self.plane_verts = np.array([[-.5,-.5,0],
                                    [-.5,.5,0],
                                    [.5,.5,0],
                                    [.5,-.5,0],
                                    [-.5,-.5,0]])
        
        Ts = np.diag([1.74,2.74,1]) #ROV x-y dimensions
        self.plane_verts = self.plane_verts.dot(Ts) - self.platform_offset
        #self.plane = scene.visuals.Line(pos = self.plane_verts, width = 5, parent  = canvas.main_view.scene)
        #self.plane = scene.visuals.Line(pos = np.add(self.plane_verts , self.adcp.geometry.position[:,0]), width = 5, parent  = canvas.main_view.scene)
        
        
        cmap = mpl.cm.jet
        c = cmap(self.beam_data.flatten()).reshape(list(np.shape(self.beam_data))+[4])
        self.beam_colors = np.full([self.adcp.config.number_of_beams,self.adcp.n_ensembles],
                          vispy.color.color_array.ColorArray)
        for b in range(self.adcp.config.number_of_beams):
            for e in range(self.adcp.n_ensembles):
                self.beam_colors[b,e] = vispy.color.color_array.ColorArray(color= c[b,:,e,:], alpha=1, clip=True, color_space='rgb')
                

        self.beam_verts = [] # store relative positions of the beams including origin
        self.beam_lines = []
        self.beam_labels = []
        for i in range(self.adcp.config.number_of_beams):
            origin = self.adcp.geometry.relative_beam_origin[:,i] 
            #pos = np.add(self.adcp.beam_midpoint_positions[i].T,self.adcp.geometry.position[:,0])
            
            pos = np.zeros((self.adcp.config.number_of_cells+1,3), dtype = float)
            pos[1:,:] = self.adcp.geometry.relative_beam_midpoint_positions[i].T
            pos[0,:] = origin
            self.beam_verts.append(pos)
           # pos = np.add(pos,self.adcp.geometry.position[:,0])

            
            self.beam_lines.append(scene.visuals.Line(pos = self.adcp_absolute_beam_midpoint_positions[i][:,:,0].T,
                                                width = 5,
                                                color = self.beam_colors[i,0],
                                                parent =canvas.main_view.scene))   
            
            
            
            
            self.beam_labels.append(scene.visuals.Text(f'beam {i+1}',
                                                      color='white',
                                                      rotation=0,
                                                      font_size = 1500,
                                                      pos = np.add(pos,self.adcp.geometry.position[:,0])[-1],
                                                      parent=canvas.main_view.scene) )
            
        self.beam_origin = scene.visuals.Markers(pos = np.add(self.adcp.geometry.position[:,0],self.adcp.geometry.relative_beam_origin.T), size = 3,parent =canvas.main_view.scene)     
        self.asset_label  = scene.visuals.Text(self.name,
                                                  color='white',
                                                  rotation=0,
                                                  font_size = 500,
                                                  pos = self.adcp.geometry.position[:,0]- self.platform_offset,
                                                  parent=canvas.main_view.scene) 
        
        
        self.ax = scene.visuals.XYZAxis(parent=canvas.main_view.scene)
        #print(type(self.ax.pos))
        
        self.ref_verts = self.ax.pos # store unit verticies
        
        
        self.ax.set_data(pos = 5*self.ref_verts + self.adcp.geometry.position[:,0] )


        # self.ax = scene.visuals.XYZAxis(pos = self.adcp.geometry.position[:,0], parent=canvas.main_view.scene)
                                   
                                   

        
    def update(self,canvas):
        t,curr_time = sim_params.get_sim_params()    
        
        
        #print(t,curr_time)
        t = np.argmin(abs(curr_time - self.timesteps))
        
        #print(t,self.timesteps[t])
        ## find the index of the closest time
        
        
        
        
        # self.asset_label.transform = STTransform(scale=(1, 1, 1), translate=self.adcp.geometry.position[:,t]-self.adcp.geometry.position[:,t-1])
        
        
        ## Build the rotation matrix
        yaw   = self.adcp.geometry.orientation[2][t]
        pitch = self.adcp.geometry.orientation[0][t]
        roll  = self.adcp.geometry.orientation[1][t]
        R = np.dot(ptools.gen_rot_x(roll),ptools.gen_rot_z(yaw).dot(ptools.gen_rot_y(pitch)))
        
    
        # update the platform (ROV)
        X = np.add(self.plane_verts.dot(R), self.adcp.geometry.position[:,t])
        self.plane.set_data(pos= X, width = 1)
        
        
        ## update the beams
        for b in range(self.adcp.config.number_of_beams):
            self.beam_lines[b].set_data(pos = self.adcp_absolute_beam_midpoint_positions[b][:,:,t].T,
                                        color = self.beam_colors[b,t])
            self.beam_labels[b].pos = self.adcp_absolute_beam_midpoint_positions[b][:,:,t].T[-1]
        
        # self.asset_label.pos = self.adcp_absolute_beam_midpoint_positions[b][:,:,t].T[-1] - self.platform_offset
        # # self.ax.pos = self.adcp.geometry.position[:,t]
        
        # self.beam_origin.set_data(pos = np.add(self.adcp.geometry.position[:,t],self.adcp.geometry.relative_beam_origin.T) )


        if t>0 and t<len(self.timesteps):
            canvas.main_view.camera.center = self.adcp.geometry.position[:,t]
            #print(canvas.main_view.camera.center)
        ## function to update the Asset

class Fixed_ADCP:
    # y is the forward direction
    def __init__(self,name,adcp):
        # contains data 
        self.name = name # name of the asset 
        self.adcp = adcp
        
        self.platform_offset = np.array([0,0,0]) # position of the center of the instrument platform (e.g., vessel) relative to the position measurement. 
        
        self.platform_width = 1
        self.platform_height = 0
        self.platform_length = 1
       
        self.adcp_absolute_beam_midpoint_positions = adcp.geometry.get_absolute_beam_midpoint_positions()
        
        u,v,z,du,dv,dz,errv = adcp.get_velocity()
        self.du = du
        self.dv = dv
        self.dz = dz
        
        
        self.beam_data = adcp.get_ensemble_array(field_name = 'ABSOLUTE BACKSCATTER')
        

         
    def init_plot(self,canvas):
        
        # scene.visuals.Line(pos =  self.adcp.geometry.position.T, width = .1, parent  = canvas.main_view.scene)
        
        ## reference axis
        self.ax = scene.visuals.XYZAxis(parent=canvas.main_view.scene)
        self.ref_verts = self.ax.pos # store unit verticies
        self.ax.set_data(pos = 5*self.ref_verts + self.adcp.geometry.position[:,0] + np.array((-1,-1,0)) )
        
        
        
        ## platform reference plane
        self.plane_verts = np.array([[-.5,-.5,0],
                                    [-.5,.5,0],
                                    [.5,.5,0],
                                    [.5,-.5,0],
                                    [-.5,-.5,0]])
        
        Ts = np.diag([self.platform_width,self.platform_length,self.platform_height]) #ROV x-y dimensions
        self.plane_verts = self.plane_verts.dot(Ts) - self.platform_offset
        self.plane = scene.visuals.Line(pos = np.add(self.plane_verts , self.adcp.geometry.position[:,0]), width = 5, parent  = canvas.main_view.scene)
        
        ## platform label
        self.asset_label  = scene.visuals.Text(self.name,
                                                  color='white',
                                                  rotation=0,
                                                  font_size = 500,
                                                  pos = self.adcp.geometry.position[:,0]- self.platform_offset,
                                                  parent=canvas.main_view.scene) 
        
        
        cmap = mpl.cm.jet
        c = cmap(self.beam_data.flatten()).reshape(list(np.shape(self.beam_data))+[4])
        self.beam_colors = np.full([self.adcp.config.number_of_beams,self.adcp.n_ensembles],
                          vispy.color.color_array.ColorArray)
        for b in range(self.adcp.config.number_of_beams):
            for e in range(self.adcp.n_ensembles):
                self.beam_colors[b,e] = vispy.color.color_array.ColorArray(color= c[b,:,e,:], alpha=1, clip=True, color_space='rgb')
                
                
        
        ## ADCP Beams
        self.beam_verts = [] # store relative positions of the beams including origin
        self.beam_lines = []
        self.beam_labels = []
        for i in range(self.adcp.config.number_of_beams):
            origin = self.adcp.geometry.relative_beam_origin[:,i] 
            pos = np.zeros((self.adcp.config.number_of_cells+1,3), dtype = float)
            pos[1:,:] = self.adcp.geometry.relative_beam_midpoint_positions[i].T
            pos[0,:] = origin
            cmap = mpl.cm.bone_r
            

            self.beam_verts.append(pos)
            self.beam_lines.append(scene.visuals.Line(pos = self.adcp_absolute_beam_midpoint_positions[i][:,:,0].T,
                                                width = 5,
                                                color = self.beam_colors[i][0],
                                                parent =canvas.main_view.scene))   
            self.beam_labels.append(scene.visuals.Text(f'beam {i+1}',
                                                      color='white',
                                                      rotation=0,
                                                      font_size = 1500,
                                                      pos = np.add(pos,self.adcp.geometry.position[:,0])[-1],
                                                      parent=canvas.main_view.scene) )
        ## beam origin points    
        self.beam_origin = scene.visuals.Markers(pos = np.add(self.adcp.geometry.position[:,0],self.adcp.geometry.relative_beam_origin.T), size = 3,parent =canvas.main_view.scene)     
        
        

        
        ## progressive vector plots 
        self.progv = []
        self.start_bin = 1
        self.end_bin = 12#self.adcp.config.number_of_cells
        pos = np.add(self.calculate_progv(0,10,self.start_bin,self.end_bin).T,self.adcp.geometry.position[:,0])
        
        
        for b in range(self.end_bin-self.start_bin):
            self.progv.append(scene.visuals.Line(pos = pos[:,b,:],
                                                width = 3,
                                                parent =canvas.main_view.scene))
            
            
        
            
        
        
        ## absolute backscatter 
        
        # self.beam_color_data = []
        # PCV_cmap = cmocean.cm.gray
        # for i in range(self.adcp.config.number_of_beams):
            
        #     PCV_carray = vispy.color.color_array.ColorArray(color=PCV_cmap(np.ones(len(PCV_df))), alpha=.1, clip=True, color_space='rgb')
        
        

            
        
        
        
            
            
        
        
        

      
    def calculate_progv(self,start_ens,end_ens,start_bin,end_bin):
        
        pos = np.zeros((3,end_bin-start_bin,(end_ens - start_ens)+1))
        
        # pos[0,:,1:] = gaussian_filter1d(np.nancumsum(np.flip(self.du[start_bin:end_bin,start_ens:end_ens],axis = 1),axis = 1),1)
        # pos[1,:,1:] = gaussian_filter1d(np.nancumsum(np.flip(self.dv[start_bin:end_bin,start_ens:end_ens],axis = 1),axis = 1),1)
        # pos[2,:,1:] = gaussian_filter1d(np.nancumsum(np.flip(self.dz[start_bin:end_bin,start_ens:end_ens],axis = 1),axis = 1),1)
        
        pos[0,:,1:] = np.nancumsum(np.flip(self.du[start_bin:end_bin,start_ens:end_ens],axis = 1),axis = 1)
        pos[1,:,1:] = np.nancumsum(np.flip(self.dv[start_bin:end_bin,start_ens:end_ens],axis = 1),axis = 1)
        pos[2,:,1:] = np.nancumsum(np.flip(self.dz[start_bin:end_bin,start_ens:end_ens],axis = 1),axis = 1)
        
        pos[2] = np.add(self.adcp.geometry.get_bin_midpoints()[start_bin:end_bin],pos[2].T).T
        
 
        #pos = gaussian_filter1d(pos,sigma = 1)
        return pos 

                            

        
    def update(self):
        t,curr_time = sim_params.get_sim_params()     
        
        # self.asset_label.transform = STTransform(scale=(1, 1, 1), translate=self.adcp.geometry.position[:,t]-self.adcp.geometry.position[:,t-1])
        
        
        ## Build the rotation matrix
        yaw   = self.adcp.geometry.orientation[2][t]
        pitch = self.adcp.geometry.orientation[0][t]
        roll  = self.adcp.geometry.orientation[1][t]
        R = np.dot(ptools.gen_rot_x(roll),ptools.gen_rot_z(yaw).dot(ptools.gen_rot_y(pitch)))
        
    
        # update the platform (ROV)
        X = np.add(self.plane_verts.dot(R), self.adcp.geometry.position[:,t])
        self.plane.set_data(pos= X, width = 1)
        
        
        ## update the beams
        for b in range(self.adcp.config.number_of_beams):
            self.beam_lines[b].set_data(pos = self.adcp_absolute_beam_midpoint_positions[b][:,:,t].T,
                                        color = self.beam_colors[b][t],)
            self.beam_labels[b].pos = self.adcp_absolute_beam_midpoint_positions[b][:,:,t].T[-1]
        
        self.asset_label.pos = self.adcp.geometry.position[:,t]- self.platform_offset
        # self.ax.pos = self.adcp.geometry.position[:,t]
        
        self.beam_origin.set_data(pos = np.add(self.adcp.geometry.position[:,t],self.adcp.geometry.relative_beam_origin.T) )



        #self.progv.set_data(pos = np.add(self.calculate_progv(t,t+10)[:,4,:].T,self.adcp.geometry.position[:,t]))
        
        pos = np.add(self.calculate_progv(t,t+10,self.start_bin,self.end_bin).T,self.adcp.geometry.position[:,t])
        for b in range(self.end_bin-self.start_bin):
            self.progv[b].set_data(pos = pos[:,b,:])
        
        ## function to update the Asset        

        
         
         
#%%
##To Do 

# Update CanvasWrapper to accept the Asset object and have global simulation parameters
# Before plotting resample all asset data to simulation timestep         
        

class SimParams:
    def __init__(self,timesteps):
        
        self.timestep = 1
        self.timesteps = timesteps
        
        self.t = 0
        self.curr_time = self.timesteps[self.t]
    
    def advance(self):
        # advance the simulation one timestep
        self.t = (self.t+self.timestep)%(len(self.timesteps))
        self.curr_time = self.timesteps[self.t]
        
    
    def get_sim_params(self):
        return self.t,self.curr_time
        

    
class CanvasWrapper:
    def __init__(self, assets,sim_params):
        
        #% Global Simulation Parameters 

        
        
        ##
        
        self.canvas = scene.SceneCanvas(keys='interactive',
                                        title='NORI-D Data Viewer',
                                        show=True,
                                        bgcolor = 'black',
                                        size=(1800, 1000))
        
        self.grid =  self.canvas.central_widget.add_grid()
        self.main_view =  self.grid.add_view(row=0,
                                             col=0,
                                             row_span=10,
                                             col_span = 10) # main viewer window
        
        #window for displaying company logos
        self.icon_view = self.grid.add_view(row=9,
                                            col=1,
                                            col_span = 4,
                                            row_span = 1,
                                            margin = 1,
                                            padding = 1) 
        
        #window for displaying company logos
        self.time_view = self.grid.add_view(row=8,
                                            col=7,
                                            col_span = 3,
                                            row_span =2,
                                            margin = 1,
                                            padding = 1) 
        

        self.assets = assets
        
        
        
        ## Setup the plot objects 
        self.time_display = scene.visuals.Text(sim_params.timesteps[0].strftime("%d-%b-%y %H:%M:%S"),
                                          color='white',
                                          rotation=0,
                                          font_size = 15,
                                          pos = (380,130),
                                          parent=self.time_view.scene) 
        


        for asset in self.assets:
            asset.init_plot(self)
            
        self.main_view.camera = "turntable" #'arcball' 
    
        # self.main_view.camera.zoom(2) 

        
        





class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, canvas_wrapper: CanvasWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)

        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()

        self.setWindowTitle("SET TITLE")
        # self.setWidth(1800)
        # self.setFixedHeight(1000)

        self.setGeometry(25, 25, 1800, 1000)

        
        self._canvas_wrapper = canvas_wrapper
        main_layout.addWidget(self._canvas_wrapper.canvas.native)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)   
        
        
        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        
        self.paused = False # paused indicator variable 

        # creating a QWidget object
        widget = QtWidgets.QWidget(self)
 
        # creating a vertical box layout
        layout = QtWidgets.QVBoxLayout(self)
 
        # push button 1
        self.PausePlayButton = QtWidgets.QPushButton("Pause", self)
        self.PausePlayButton.clicked.connect(self.pause_play)
        #self.StartButton.valueChanged[int].connect(self.pause_play)
        
        # time slider 
        self.TimeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.TimeSlider.setRange(0,len(sim_params.timesteps))
        self.TimeSlider.valueChanged[int].connect(self.update_time)
        
        # timestep dial
        self.TimestepDial = QtWidgets.QDial()
        self.TimestepDial.valueChanged.connect(self.update_timestep)
        self.TimestepDial.setRange(-10,10)
        self.TimestepDial.setNotchesVisible(True)
        self.TimestepDial.setGeometry(220, 125, 200, 60)
        self.DialLabel = QtWidgets.QLabel(f"dt = {sim_params.timestep} min", self)
        self.DialLabel.setAlignment(Qt.AlignCenter)
        self.DialLabel.setGeometry(400, 125, 200, 60)
        
        # adding these buttons to the layout
        layout.addWidget(self.PausePlayButton)
        layout.addWidget(self.TimeSlider)
        layout.addWidget(self.DialLabel)
        layout.addWidget(self.TimestepDial)
        
        # setting the layout to the widget
        
        widget.setLayout(layout)
        widget.setAutoFillBackground(True)
        
        # Playback Dock Popout Window 
        self.PlaybackDock=QtWidgets.QDockWidget('Playback',self)
        self.PlaybackDock.setFixedSize(200, 300)
        self.PlaybackDock.setWidget(widget)        
        self.PlaybackDock.setGeometry(100, 0, 200, 30)
        self.PlaybackDock.setAllowedAreas(Qt.NoDockWidgetArea)

        
    def update_timestep(self):
        sim_params.timestep = self.TimestepDial.value()
        self.DialLabel.setText(f"dt = {sim_params.timestep} min")
        
        
    def update_time(self):
        sim_params.t = self.TimeSlider.value()
        #canvas.main_view.update()
        
    def pause_play(self):
        if not self.paused:
            timer.stop()
            self.paused = True
            self.PausePlayButton.setText('Play')
        else:
            timer.start()
            self.paused = False
            self.PausePlayButton.setText('Pause')
        
        
    def closeEvent(self, event):
        timer.stop()

        


def update(ev):
    
    sim_params.advance()
    t,curr_time = sim_params.get_sim_params()
    
    win.TimeSlider.setValue(t)
    canvas.time_display.text =  f't={t}'.ljust(10) + curr_time.strftime("%d-%b-%y %H:%M:%S")
    
    for asset in canvas.assets:
        
        #try:
        asset.update(canvas,sim_params)
        #except: print('failed update')

    
    

    
def run(assets,timesteps):

    global timer,canvas,app,win,sim_params
    
    
    sim_params = SimParams(timesteps = timesteps)
      
    app = use_app("pyqt5")
    app.create()
    
    
    canvas = CanvasWrapper(sim_params= sim_params, assets = assets)
    win = MainWindow(canvas)
    
    
    #timer = Timer('auto', connect=update, start=True, app = app)
    timer = Timer('auto' ,connect=update, start=True, app = app)
    win.destroyed.connect(timer.stop)
    
    win.show()
    app.run()    
  

#def run():


# assets =[ IP_ROV(name = 'ROV ADCP', adcp = adcp)]



# run(assets,timesteps = adcp.get_ensemble_datetimes())
    


#%%

# if __name__ == '__main__':
#     # assets =[data_visualizer.ROV_ADCP_Asset(name = 'HAIN', adcp = adcp1),
#     #           data_visualizer.ROV_ADCP_Asset(name = 'USBL', adcp = adcp1)]  
    
    
#     # assets =[data_visualizer.ROV_ADCP_Asset(name = 'HAIN', adcp = adcp1),
#     #           data_visualizer.ROV_ADCP_Asset(name = 'TEST', adcp = adcp1b)]  
    
#     assets =[data_visualizer.ADCP_Asset(name = 'USBL', adcp = adcp)]  
#     data_visualizer.run(assets = assets,timesteps = adcp.ensemble_times)


