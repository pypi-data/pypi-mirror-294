# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 11:46:59 2023

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

##sys.path.insert(1, r'C:\Users\anba\Desktop\Projects\pyplume\pyplume\ptools')
##import ptools

# # from matplotlib_dhi import subplots 
# # import adcp_plot_tools

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd, numpy as np


from ..ptools import ptools

#%%



#%%

class PCV:
    def __init__(self,st,et,set_focus = False):
        self.update_count = 0
        self.set_focus = set_focus
        self.st = st
        self.et = et

        
    def init_plot(self,canvas):
        
        
        
        path = r'P:\41806287\41806287 NORI-D Data\Data\PCV\Position\Processed\02 PCV Tracks\02_PCV_Tracks.csv'
        PCV_df = pd.read_csv(path, index_col = [0], parse_dates = True)
        PCV_df.index = PCV_df.index.tz_localize(None)
        mask = (PCV_df.index >= self.st) & (PCV_df.index<=self.et)
        self.df = PCV_df.loc[mask]
        
        
  
        
        
        
        
        self.df['depth'] = -self.df['depth']
        self.df['depth'].loc[self.df['depth']>-4100] = np.mean(self.df['depth'])
        

    

        self.timesteps = np.array(self.df.index.tolist())
        
        self.pos = np.array([self.df['easting'].tolist(),self.df['northing'].tolist(),self.df['depth'].tolist()]).T
        #PCV_carray = vispy.color.color_array.ColorArray(color=PCV_cmap(np.ones(len(PCV_df))), alpha=.1, clip=True, color_space='rgb')
        # scene.visuals.Line(pos =  self.adcp.geometry.position.T, width = .1, parent  = canvas.main_view.scene)

        self.PCV_tracks = scene.visuals.Markers(pos = self.pos, size = 5,parent =canvas.main_view.scene, face_color = 'white', edge_color = 'white')     


        self.PCV_pos =  scene.visuals.Markers(pos = self.pos[0:2,:], size = 15,parent =canvas.main_view.scene)   

        # self.ax = scene.visuals.XYZAxis(pos = self.adcp.geometry.position[:,0], parent=canvas.main_view.scene)
                                   
                                   

        
    def update(self,canvas,sim_params):
       t,curr_time = sim_params.get_sim_params()    
       
       #idx = self.df.index.get_indexer([curr_time],method = 'nearest')
       t = np.argmin(abs(curr_time - self.timesteps)) 
       
       #print(t)
       
       self.PCV_pos.set_data(pos = self.pos[t:(t+1),:])
       
       if self.set_focus:
           canvas.main_view.camera.center = self.pos[t,:] 
       
class RiserReturn:
    def __init__(self,st,et,set_focus = False):
        self.update_count = 0
        self.set_focus = set_focus
        self.st = st
        self.et = et

        
    def init_plot(self,canvas):
        
        
        
        path = r'P:\41806287\41806287 NORI-D Data\Data\Vessel\Hidden Gem\Riser Return\Processed\Position\02_midwater_discharge_position.csv'
        PCV_df = pd.read_csv(path, index_col = [0], parse_dates = True)
        PCV_df.index = PCV_df.index.tz_localize(None)
        mask = (PCV_df.index >= self.st) & (PCV_df.index<=self.et)
        self.df = PCV_df.loc[mask]
        
        
  
        
        
        
        
        self.df['depth'] = -self.df['depth']
        #self.df['depth'].loc[self.df['depth']>-4100] = np.mean(self.df['depth'])
        

    

        self.timesteps = np.array(self.df.index.tolist())
        
        self.pos = np.array([self.df['easting'].tolist(),self.df['northing'].tolist(),self.df['depth'].tolist()]).T
        #PCV_carray = vispy.color.color_array.ColorArray(color=PCV_cmap(np.ones(len(PCV_df))), alpha=.1, clip=True, color_space='rgb')
        # scene.visuals.Line(pos =  self.adcp.geometry.position.T, width = .1, parent  = canvas.main_view.scene)

        self.PCV_tracks = scene.visuals.Markers(pos = self.pos, size = .1,parent =canvas.main_view.scene, face_color = 'gray', edge_color = 'gray')     


        self.PCV_pos =  scene.visuals.Markers(pos = self.pos[0:2,:], size = 1000,parent =canvas.main_view.scene, spherical = True, symbol = 's', face_color = 'yellow')   

        # self.ax = scene.visuals.XYZAxis(pos = self.adcp.geometry.position[:,0], parent=canvas.main_view.scene)
                                   
                                   

        
    def update(self,canvas,sim_params):
       t,curr_time = sim_params.get_sim_params()    
       
       #idx = self.df.index.get_indexer([curr_time],method = 'nearest')
       t = np.argmin(abs(curr_time - self.timesteps)) 
       
       #print(t)
       
       self.PCV_pos.set_data(pos = self.pos[t:(t+1),:])
              
       
       #print(t,curr_time)
       #t = np.argmin(abs(curr_time - self.timesteps))                    
       
       if self.set_focus:
           canvas.main_view.camera.center = self.pos[t,:]    
        
class Bathymetry:
     
     def __init__(self):
         # contains data 
         
         #self.default_mesh = load_data_file(r'C:\Users\anba\OneDrive - DHI\Desktop\Visualization\Bathymetry\Mesh\local_bathy_mesh.obj')
         
         self.default_mesh = load_data_file(r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\GIS\Data Analytics\mesh\NORI_D_CTA_AUV_MBES2040_50cm_CLIPPED_FILLED.obj')
         self.texture_path = load_data_file(r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\GIS\Data Analytics\mesh\NORI_D_CTA_AUV_MBES2040_50cm_CLIPPED_FILLED.png')
         
         
         
         
         self.lease_area_xyz = pd.read_csv(r'P:\41806287\41806287 NORI-D Data\GIS\Data Analytics\point_clouds\LeaseArea.xyz', header = None)[[0,1,2]].to_numpy()
         self.pcv_tracks_xyz = pd.read_csv(r'P:\41806287\41806287 NORI-D Data\GIS\Data Analytics\point_clouds\PCV_Tracks.xyz', header = None)[[0,1,2]].to_numpy()
         self.contours_xyz = pd.read_csv(r'P:\41806287\41806287 NORI-D Data\GIS\Data Analytics\point_clouds\Contours.xyz', header = None, delimiter = '|')[[0,1,2]].to_numpy()
         
         
     def init_plot(self,canvas):


         
   
         
        vertices, faces, normals, texcoords = read_mesh(self.default_mesh)
        mesh = Mesh(vertices, faces, color=(1, 1, 1, 0.8))
        shading_filter1 = ShadingFilter(shininess=100, shading = 'smooth', ambient_light = (1,1,1,0.5), diffuse_light = (1,1,1,0.75),specular_light=(1, 1, 1, 0.75))
        mesh.attach(shading_filter1)
         
         
        scene.visuals.Line(pos = self.lease_area_xyz, width = 5, color = 'red',parent  = canvas.main_view.scene)
        
        

        
        #scene.visuals.Markers(pos = self.pcv_tracks_xyz, size = 1, face_color = 'black',scaling =False, parent  = canvas.main_view.scene)
        
        #scene.visuals.Markers(pos = self.contours_xyz, size = 1, face_color = 'black',scaling =False, parent  = canvas.main_view.scene)
        # print(np.shape(texcoords))
        # texture = np.flipud(vispy.io.image.read_png(self.texture_path))
        
        
        # texture_filter = TextureFilter(texture, texcoords)
        # mesh.attach(texture_filter)
        

         
        canvas.main_view.add(mesh)
        
        
        def attach_headlight(view):
            light_dir = (0, 1, 0, 0)      
            shading_filter1.light_dir = light_dir[:3]
            initial_light_dir = view.camera.transform.imap(light_dir)
            @canvas.main_view.scene.transform.changed.connect
            def on_transform_change(event):
                transform = view.camera.transform
                shading_filter1.light_dir = transform.map(initial_light_dir)[:3]
        
        
        attach_headlight(canvas.main_view)
        
         
     def update(self,canvas,sim_params):
        #canvas.main_view.camera.zoom(10) 
        None
        
        
        


class ADCP:
    

    def __init__(self,adcp,set_focus = False,platform = 'ROV',**kwargs):
        
        
        self.name = kwargs.pop('name','ADCP')
        self.adcp = adcp
        self.set_focus = set_focus
        
        ## reference platform geometry 
        self.platform_offset = kwargs.pop('platform_offset',np.array([-0.36,-1.45,-0.31])) # position of the center of the instrument platform (e.g., vessel) relative to the position measurement. 
        self.platform_width = kwargs.pop('platform_width',1.74)
        self.platform_height = kwargs.pop('platform_height',2.74)
        
        
        self.platform = platform
        ## load time dependent plot data into memory
        

        
        self.position = self.adcp.geometry.pose.pose[['x','y','z']].to_numpy().T
        
        
        self.orientation = self.adcp.geometry.pose.pose[['roll','pitch','heading']].to_numpy().T
        self.adcp_absolute_beam_midpoint_positions = adcp.geometry.get_absolute_beam_midpoint_positions()
        
        
        # if adcp.geometry.pose.z_convention == 'reverse':
        #     self.position[2] = -self.position[2]
        #     self.adcp_absolute_beam_midpoint_positions[2] = -self.adcp_absolute_beam_midpoint_positions[2]
        
    
        self.beam_data = adcp.get_ensemble_array(field_name = 'ABSOLUTE BACKSCATTER')
        self.timesteps = adcp.get_ensemble_datetimes()
 
        if self.platform == 'Lander':
            u,v,z,self.du,self.dv,self.dz,errv = adcp.get_velocity()
            
            
            self.du[:,0] = 0
            self.du[:,12:] = 0

            self.dv[:,0]  = 0
            self.dv[:,12:] = 0
            
            self.dz[:,0]  = 0
            self.dz[:,12:] = 0
        
    def init_plot(self,canvas):
        """
        Initalize vispy scene objects 

        Parameters
        ----------
        canvas : vispy.scene.canvas object
            canvas to plot to.

        Returns
        -------
        None.

        """
        
        
        
        # scene.visuals.Line(pos =  self.adcp.geometry.position.T, width = .1, parent  = canvas.main_view.scene)
        xrng = np.nanmax(self.position[0]) - np.nanmin(self.position[0])
        yrng = np.nanmax(self.position[0]) - np.nanmin(self.position[0])
        
        
    
        # grid = scene.visuals.GridLines(scale = (1/.1,1/.1))
        # canvas.main_view.add(grid)
        
        ######################## plot the platform ############################
        ## normalized reference platform vertices (centered about xy = 0)
        self.plane_verts = np.array([[-.5,-.5,0],
                                    [-.5,.5,0],
                                    [.5,.5,0],
                                    [.5,-.5,0],
                                    [-.5,-.5,0]])
        
        Ts = np.diag([self.platform_width,self.platform_height,0]) 
        self.plane_verts = self.plane_verts.dot(Ts) - self.platform_offset
        self.plane = scene.visuals.Line(pos = np.add(self.plane_verts , self.position[:,0]), width = 5, parent  = canvas.main_view.scene)
        
        
        
        ############### plot the individual beams ############################
        
        
        ## generate beam color arrays
        cmap = mpl.cm.turbo
        
        # ## normalize color data 
        # def normalize(x,minval = -50,maxval = 150):
        #     '''
        #     normalize data in x between 0 and over the interval [global_minval,global_maxval ]
        

        #     Parameters
        #     ----------
        #     x : numpy array
        #         DESCRIPTION.
        #     minval : TYPE, optional
        #         DESCRIPTION. The default is -50.
        #     maxval : TYPE, optional
        #         DESCRIPTION. The default is 150.

        #     Returns
        #     -------
        #     None.
            
        #     '''
            
            
        #     xnorm = x - minval
        #     xnorm = x/(maxval - minval)
            
        #     return (x-minval)/(maxval - minval)
            
        
        norm = mpl.colors.Normalize(vmin=-95, vmax=-45)
        c = cmap(norm(self.beam_data.flatten())).reshape(list(np.shape(self.beam_data))+[4])
        
        
        
        self.beam_colors = np.full([self.adcp.config.number_of_beams,self.adcp.n_ensembles],
                          vispy.color.color_array.ColorArray)
        for b in range(self.adcp.config.number_of_beams):
            for e in range(self.adcp.n_ensembles):
                self.beam_colors[b,e] = vispy.color.color_array.ColorArray(color= c[b,:,e,:], alpha=1)#, clip=False, color_space='rgb')
                


        
        self.beam_verts = [] # store relative positions of the beams including origin
        self.beam_lines = []
        self.beam_points = []
        self.beam_labels = []
        for i in range(self.adcp.config.number_of_beams):
            origin = self.adcp.geometry.relative_beam_origin[:,i] # origin of the beam 
            pos = np.zeros((self.adcp.config.number_of_cells+1,3), dtype = float)
            pos[1:,:] = self.adcp.geometry.relative_beam_midpoint_positions[i].T
            pos[0,:] = origin
            # self.beam_verts.append(pos)
            
           # pos = np.add(pos,self.adcp.geometry.position[:,0])

            
            self.beam_lines.append(scene.visuals.Line(pos = self.adcp_absolute_beam_midpoint_positions[:,i,:,0].T,
                                                width = 5,
                                                color = self.beam_colors[i,0],
                                                parent =canvas.main_view.scene))   
            
            
            self.beam_points.append(scene.visuals.Markers(pos = self.adcp_absolute_beam_midpoint_positions[:,i,:,0].T,
                                                          size = .5,
                                                          parent = canvas.main_view.scene))
            
            
            
            
            self.beam_labels.append(scene.visuals.Text(f'beam {i+1}',
                                                      color='white',
                                                      rotation=0,
                                                      font_size = 1500,
                                                      pos = np.add(pos,self.position[:,0])[-1],
                                                      parent=canvas.main_view.scene) )
            
        self.beam_origin = scene.visuals.Markers(pos = np.add(self.position[:,0],self.adcp.geometry.relative_beam_origin.T), size = 3,parent =canvas.main_view.scene)     
        self.asset_label  = scene.visuals.Text(self.name,
                                                  color='white',
                                                  rotation=0,
                                                  font_size = 500,
                                                  pos = self.position[:,0]- 5*self.platform_offset,
                                                  parent=canvas.main_view.scene) 
        
        
        self.ax = scene.visuals.XYZAxis(parent=canvas.main_view.scene)
        
        self.ref_verts = self.ax.pos # store unit verticies
        
        
        self.ax.set_data(pos = 5*self.ref_verts + self.position[:,0] )


    def update(self,canvas,sim_params):
        t,curr_time = sim_params.get_sim_params()    
        
        
        #print(t,curr_time)
        t = np.argmin(abs(curr_time - self.timesteps))                    
        
        
        
        if t>0 and t<len(self.timesteps):
            ## Build the rotation matrix
            yaw   = self.orientation[2][t]
            pitch = self.orientation[0][t]
            roll  = self.orientation[1][t]
            R = np.dot(ptools.gen_rot_x(roll),ptools.gen_rot_z(yaw).dot(ptools.gen_rot_y(pitch)))
            
            
            # update the platform (ROV)
            X = np.add(self.plane_verts.dot(R), self.position[:,t])
            self.plane.set_data(pos= X, width = 1)
            
            
            ## update the beams
            
            
            for b in range(self.adcp.config.number_of_beams):
                self.beam_lines[b].set_data(pos = self.adcp_absolute_beam_midpoint_positions[:,b,:,t].T,
                                            color = self.beam_colors[b,t])
                self.beam_labels[b].pos = self.adcp_absolute_beam_midpoint_positions[:,b,:,t].T[-1]
                
                
                if self.platform == 'Lander':
                    lag_dist = 100
                    if t>lag_dist:
                    
                        pos = self.adcp_absolute_beam_midpoint_positions[:,b,:,t-lag_dist:t].T
                        pos = pos.reshape((lag_dist)*pos.shape[1],3)
                        
                        
                        ## offset by progressive vector 
                        pu = np.nancumsum(np.flip(self.du[t-lag_dist:t,:]),axis = 0) #,-np.outer(du[0,:],np.ones(self.n_ensembles)).T])
                        pv = np.nancumsum(np.flip(self.dv[t-lag_dist:t,:]),axis = 0) # ,-np.outer(dv[0,:],np.ones(self.n_ensembles)).T])
                        pz = 0*np.nancumsum(np.flip(self.dz[t-lag_dist:t,:]),axis = 0) # ,-np.outer(dz[0,:],np.ones(self.n_ensembles)).T])
                        
                        
                        pu[0,:] = 0 
                        pv[1,:] = 0
                        pz[2,:] = 0
                        pvec = np.array([pu,pv,pz]).T.reshape(np.shape(pos))
                        
    
                        
                        
                    
      
                        #np.cumsum(np.flip(df['du'].iloc[start_idx:end_idx-1].tolist()).tolist())
                        #print(t)
                        all_colors = self.beam_colors[b,t-lag_dist:t].copy() # colors for all lagged timesteps 
                        #print(len(all_colors))
                        colors = self.beam_colors[b,t-lag_dist:t][0].copy()
            
                        for color in self.beam_colors[b,t-lag_dist:t][1:]:
                            colors.extend(color)
                        #print(len(colors),len(pos))     
                        if len(colors) == len(pos):
                            self.beam_points[b].set_data(pos = pos + pvec, size = 5, edge_width = .1, edge_color = colors, face_color = colors)#
                        
                elif self.platform == 'ROV':
                    lag_dist = 100
                    if t>lag_dist:
                    
                        pos = self.adcp_absolute_beam_midpoint_positions[:,b,:,t-lag_dist:t].T
                        pos = pos.reshape((lag_dist)*pos.shape[1],3)
                        
                    
      
                        #np.cumsum(np.flip(df['du'].iloc[start_idx:end_idx-1].tolist()).tolist())
                        #print(t)
                        all_colors = self.beam_colors[b,t-lag_dist:t].copy() # colors for all lagged timesteps 
                        #print(len(all_colors))
                        colors = self.beam_colors[b,t-lag_dist:t][0].copy()
            
                        for color in self.beam_colors[b,t-lag_dist:t][1:]:
                            colors.extend(color)
                        #print(len(colors),len(pos))     
                        if len(colors) == len(pos):
                            self.beam_points[b].set_data(pos = pos , size = 5, edge_width = .1, edge_color = colors, face_color = colors)#
                                    
            self.asset_label.pos = self.position[:,t]- self.platform_offset
            # self.ax.pos = self.adcp.geometry.position[:,t]
            
            self.beam_origin.set_data(pos = np.add(self.position[:,t],self.adcp.geometry.relative_beam_origin.T) )
            
            
            if self.set_focus:
                canvas.main_view.camera.center = self.position[:,t] 
                
#%%

class CTD:
    def __init__(self,ctd,set_focus = False,adcp = None,platform = 'ROV',**kwargs):
        
        
        self.name = kwargs.pop('name','CTD')
        self.ctd = ctd
        self.set_focus = set_focus
        
        ## reference platform geometry 
        self.platform_offset = kwargs.pop('platform_offset',np.array([-0.36,-1.45,-0.31])) # position of the center of the instrument platform (e.g., vessel) relative to the position measurement. 
        self.platform_width = kwargs.pop('platform_width',1.74)
        self.platform_height = kwargs.pop('platform_height',2.74)

        self.platform = platform
        self.plot_prog_v = False
        
        ## load time dependent plot data into memory
                
        self.position = self.ctd.geometry.pose.pose[['x','y','z']].to_numpy().T
        self.orientation = self.ctd.geometry.pose.pose[['roll','pitch','heading']].to_numpy().T
        self.absolute_sensor_position = ctd.geometry.get_absolute_sensor_position()
        self.sensor_data,self.timesteps = ctd.get_timeseries_data(field_name = 'Turbidity (NTU)')
        #self.timesteps = ctd.data['DateTime']
        
        
        if platform == 'Lander' and adcp:
            
            self.plot_prog_v = True
            
            # u,v,z,self.du,self.dv,self.dz,errv = adcp.get_velocity()
    
            # self.du = self.du[:,2]
            # self.dv = self.dv[:,2]
            # self.dz = self.dz[:,2]
            
            
            u,v,z,du,dv,dz,errv = adcp.get_velocity()
            t = adcp.get_ensemble_datetimes()
            du = du[:,2]
            dv = dv[:,2]
            dz = dz[:,2]
            df = pd.DataFrame(data = {'du':du,'dv':dv,'dz':dz}, index = t)
            df = df.reindex(ctd.data['DateTime'], method = 'nearest')
            df['du'].interpolate(inplace = True, method = 'time')
            df['dv'].interpolate(inplace = True, method = 'time')
            df['dz'].interpolate(inplace = True, method = 'time')
            
            self.du = df['du'].to_numpy()
            self.dv = df['dv'].to_numpy()
            self.dz = df['dz'].to_numpy()
            

        
            
        

    def init_plot(self,canvas):
        """
        Initalize vispy scene objects 

        Parameters
        ----------
        canvas : vispy.scene.canvas object
            canvas to plot to.

        Returns
        -------
        None.

        """
        
        
        
        # scene.visuals.Line(pos =  self.adcp.geometry.position.T, width = .1, parent  = canvas.main_view.scene)
        
        
        ######################## plot the platform ############################
        ## normalized reference platform vertices (centered about xy = 0)
        self.plane_verts = np.array([[-.5,-.5,0],
                                    [-.5,.5,0],
                                    [.5,.5,0],
                                    [.5,-.5,0],
                                    [-.5,-.5,0]])
        
        Ts = np.diag([self.platform_width,self.platform_height,0]) 
        self.plane_verts = self.plane_verts.dot(Ts) - self.platform_offset
        self.plane = scene.visuals.Line(pos = np.add(self.plane_verts , self.position[:,0]), width = 5, parent  = canvas.main_view.scene)
        
        
        
        ############### plot the individual beams ############################
        
        
        ## generate beam color arrays
        cmap = mpl.cm.turbo

            
        
        norm = mpl.colors.Normalize(vmin=0, vmax=100)
        c = cmap(norm(self.sensor_data))
        self.colors = vispy.color.color_array.ColorArray(color= c, alpha=1)#, clip=False, color_space='rgb')
        
        pos = self.absolute_sensor_position[:,0:2].T
 
            
        self.data_points = scene.visuals.Markers(pos = pos,size = 5,parent = canvas.main_view.scene)
            
        self.data_line = scene.visuals.Line(pos = pos,width = 5,parent = canvas.main_view.scene)    
            
   
            
            
            
 
        self.asset_label  = scene.visuals.Text(self.name,
                                                  color='white',
                                                  rotation=0,
                                                  font_size = 500,
                                                  pos = self.position[:,0]- 2*self.platform_offset,
                                                  parent=canvas.main_view.scene) 
        
        
        self.ax = scene.visuals.XYZAxis(parent=canvas.main_view.scene)
        self.ref_verts = self.ax.pos # store unit verticies
        self.ax.set_data(pos = 5*self.ref_verts + self.position[:,0] )


    def update(self,canvas,sim_params):
        t,curr_time = sim_params.get_sim_params()    
        
        
        #print(t,curr_time)
        t = np.argmin(abs(curr_time - self.timesteps))                    
        t_lag = max(np.argmin(abs((curr_time - pd.Timedelta('500 min')) - self.timesteps)),0)
        #max(t-100,0) 
        #print(t,t_lag)
        if t>0 and t<len(self.timesteps):
            ## Build the rotation matrix
            yaw   = self.orientation[2][t]
            pitch = self.orientation[0][t]
            roll  = self.orientation[1][t]
            R = np.dot(ptools.gen_rot_x(roll),ptools.gen_rot_z(yaw).dot(ptools.gen_rot_y(pitch)))
            
            
            # update the platform (ROV)
            X = np.add(self.plane_verts.dot(R), self.position[:,t])
            self.plane.set_data(pos= X, width = 1)
            
            
            ## update the beams
            
            
            # for b in range(self.adcp.config.number_of_beams):
            #     self.beam_lines[b].set_data(pos = self.adcp_absolute_beam_midpoint_positions[:,b,:,t].T,
            #                                 color = self.beam_colors[b,t])
            #     self.beam_labels[b].pos = self.adcp_absolute_beam_midpoint_positions[:,b,:,t].T[-1]
                
            #lag_dist = 10
            if t>t_lag:
            
                pos = self.absolute_sensor_position[:,t_lag:t].T
                
                
                colors = self.colors[t_lag:t]
                if self.plot_prog_v:
                    ## offset by progressive vector 
                    pu = np.nancumsum(np.flip(self.du[t_lag:t])) #,-np.outer(du[0,:],np.ones(self.n_ensembles)).T])
                    pv = np.nancumsum(np.flip(self.dv[t_lag:t])) # ,-np.outer(dv[0,:],np.ones(self.n_ensembles)).T])
                    pz = 20 + 0*np.nancumsum(np.flip(self.dz[t_lag:t])) # ,-np.outer(dz[0,:],np.ones(self.n_ensembles)).T])
                    
                    
                    pu -= pu[0] 
                    pv -= pv[1] 
                    #pz -= pz[2] = 0
                    pvec = np.array([pu,pv,pz]).T.reshape(np.shape(pos))
                    
                    pos = pos+ pvec
   
                    # colors = len(self.colors[t_lag:t])*[0]
                    # for i,color in enumerate(self.colors[t_lag:t]):
                    #     colors[-i] = color
                    #colors = np.flip(self.colors[t-lag_dist:t]) # colors for all lagged timesteps 
                    

        
                
                #self.data_points.set_data(pos =pos, size = 8, edge_width = .1, edge_color = colors, face_color = colors)#
                self.data_line.set_data(pos,width = 5,color = colors)
            self.asset_label.pos = self.position[:,t]- 3*self.platform_offset

            
            
            
            if self.set_focus:
                canvas.main_view.camera.center = self.position[:,t] 

