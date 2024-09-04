# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 15:45:10 2023

@author: anba
"""
import numpy as np
from scipy.ndimage import gaussian_filter
from ..ptools import ptools
class processing:
    
    def __init__(self,pd0):
        
        self._pd0 = pd0
        
        self.ensemble_fields = ['ECHO INTENSITY','CORRELATION MAGNITUDE','PERCENT GOOD'] # keys for fields defined in ensemble data. Can be modified by append_to_ensembles method
        
        
        #vectorize some functions
        self.water_absorption_coeff = np.vectorize(self._scalar_water_absorption_coeff)
        self.sediment_absorption_coeff = np.vectorize(self._scalar_sediment_absorption_coeff)   
        self.counts_to_absolute_backscatter = np.vectorize(self._scalar_counts_to_absolute_backscatter)


    def apply_interference_filter(self,niter = 3, dx_thresh = 0.05, sigma = None):
        
        def filter_array(X):
            """
            Generate numpy array of filterd Data (designed to remove HAIN DVL interference)
                -Two passes of column-wise spike filter, filling nan values inbetween passes by averaging neighbors.
                -Final gaussing smoothing step
            Args:
                ensemble_array: numpy array of echo intensity data with dimensions (nbins,n_ensembles)
            Returns:
                numpy array with dimensions (nbins,n_ensembles)  
        
            """     
            
            def filt(X):
                """
                column-wise spike filter - removes data with a LHS differential exceeding 0.5
                filtered values replaced by nan values. 
                
                Args:
                    X: numpy array of echo intensity data with dimensions (nbins,n_ensembles)
                Returns:
                    X_new: numpy array with dimensions (nbins,n_ensembles)  
                    X_filt: filter mask 
                """
                X_norm = X - np.nanmin(X)
                X_norm = X_norm/np.nanmax(X_norm)
                
                X_dx = np.diff(X_norm,axis = 1) # difference across rows(up/down)
                X_dy = np.diff(X_norm,axis = 0) # difference across columns(left/right)
                
                X_new =X[:,1:].copy()
                X_filt = X_dx 
                X_new[X_filt>dx_thresh] = np.nan
                return X_new,X_filt
            
        
            base_mask = np.isnan(X) # mask for originalyl nan valeus
            
            X_new = X
            for _iter in range(niter):
                X_new,X_filt = filt(X_new) # filter out entries with large x-derivative
        
                mask = np.isnan(X_new)
                X_new[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), X_new[~mask]) # fill nan values with nearest neighbor
                
            
            
            #Append first two columns back into data (these were lost during the two passes of spike filter)
            Xout = X.copy()
            
            if sigma:
                Xout[:,niter:] = gaussian_filter(X_new, sigma = sigma)
            else:
                Xout[:,niter:] = X_new
        
            Xout[base_mask] = np.nan #(nan back out originally nan values)
        
            
            return Xout
    
    
 
        X = self._pd0.get_ensemble_array(field_name = 'ECHO INTENSITY') # raw echo data

        X_filt = X
        for i in range(X.shape[0]):#loop over each beam
            X_filt[i] = filter_array(X[i])
    
        self.append_to_ensembles(X_filt,title = 'ECHO INTENSITY')
        
        

    def mask_by_platform_z(self, min_z=0, max_z=1e6):
        """
        Apply a mask to ADCP data based on platform depth (Z-coordinate).
    
        Parameters
        ----------
        min_z : float, optional
            Minimum depth in meters to include in the mask. Defaults to 0.
        max_z : float, optional
            Maximum depth in meters to include in the mask. Defaults to 1e6.
    
        Notes
        -----
        This method creates a 1D mask based on the platform's Z-coordinate and broadcasts it
        to match the dimensions of the data arrays. It then applies this mask to all ensembles,
        effectively filtering out data collected outside the specified depth range.
        """
        mask_1d = (self._pd0.geometry.pose.pose.z >= min_z) & (self._pd0.geometry.pose.pose.z <= max_z)
        mask = np.broadcast_to(mask_1d[np.newaxis, np.newaxis, :], (self._pd0.config.number_of_beams, self._pd0.config.number_of_cells, self._pd0.n_ensembles))
        self._pd0.mask.define_mask(mask=mask, name='By Platform Depth', set_active=True)
    
    def mask_by_correlation_magnitude(self, min_cmag=64, max_cmag=256):
        """
        Apply a mask based on correlation magnitude values.
    
        Parameters
        ----------
        min_cmag : int, optional
            Minimum correlation magnitude to include in the mask. Defaults to 64.
        max_cmag : int, optional
            Maximum correlation magnitude to include in the mask. Defaults to 256.
    
        Notes
        -----
        Creates and applies a mask to ADCP ensemble data based on the correlation magnitude.
        Data with correlation magnitude values outside the specified range are masked out.
        """
        X = self._pd0.get_ensemble_array(field_name='CORRELATION MAGNITUDE')
        mask = (X >= min_cmag) & (X <= max_cmag)
        self._pd0.mask.define_mask(mask, name=f'CORRELATION MAGNITUDE [{min_cmag} ,{max_cmag}]', set_active=True)
    
        
    def mask_by_signal_to_noise(self, min_stn=1, max_stn=1e4):
        """
        Apply a mask based on signal to noise ratio.
    
        Parameters
        ----------
        min_stn : float, optional
            Minimum signal to noise ratio to include in the mask. Defaults to 1.
        max_stn : float, optional
            Maximum signal to noise ratio to include in the mask. Defaults to 1e4.
    
        Notes
        -----
        Creates and applies a mask to ADCP ensemble data based on the signal to noise ratio.
        Data with signal to noise ratio values outside the specified range are masked out.
        """
        X = self._pd0.get_ensemble_array(field_name='SIGNAL TO NOISE RATIO')
        mask = (X >= min_stn) & (X <= max_stn)
        self._pd0.mask.define_mask(mask, name=f'SIGNAL TO NOISE RATIO [{min_stn} ,{max_stn}]', set_active=True)
    
        
    def mask_by_absolute_backscatter(self, min_abs=-95, max_abs=0):
        """
        Apply a mask based on absolute backscatter values.
    
        Parameters
        ----------
        min_abs : int, optional
            Minimum absolute backscatter value to include in the mask. Defaults to -95 dB.
        max_abs : int, optional
            Maximum absolute backscatter value to include in the mask. Defaults to 0 dB.
    
        Notes
        -----
        Creates and applies a mask to ADCP ensemble data based on the absolute backscatter values.
        Data with absolute backscatter values outside the specified range are masked out.
        """
        X = self._pd0.get_ensemble_array(field_name='ABSOLUTE BACKSCATTER')
        mask = (X >= min_abs) & (X <= max_abs)
        self._pd0.mask.define_mask(mask, name=f'ABSOLUTE BACKSCATTER [{min_abs} ,{max_abs}]', set_active=True)
                
    def mask_bottom_track(self, cell_offset=0, spike_filter=False, spike_window=10, spike_thresh=5):
        """
        Create a mask based on the ADCP bottom track data, optionally applying a rolling spike filter.
    
        Parameters
        ----------
        cell_offset : int, optional
            The number of cells to mask above (positive) or below (negative) the bottom-track cell.
            Defaults to 0, which masks the bottom track cell itself.
        spike_filter : bool, optional
            Whether to apply a spike filtering to the bottom track data before creating the mask.
            Defaults to False.
        spike_window : int, optional
            The window size for the rolling spike filter. Only used if spike_filter is True.
            Defaults to 10.
        spike_thresh : int, optional
            The threshold factor for spike detection in the rolling spike filter. Only used if
            spike_filter is True. Defaults to 5.
    
        Notes
        -----
        This method calculates the ADCP bottom track range either directly or with a spike filter,
        then creates a mask that marks cells as being above or below the bottom track based on
        the specified offset. This mask is then applied to the ADCP data to filter out cells
        affected by proximity to the seabed or other reflective surfaces.
        """
        offset_distance = self._pd0.config.depth_cell_length * cell_offset
    
        if spike_filter:
            bt_range = self._pd0.get_bottom_track()
            
            for i in range(bt_range.shape[0]):
                bt_range[i] = ptools.rolling_spike_filter(bt_range[i] , window_size=spike_window, threshold_factor=spike_thresh)
        else:
            bt_range = self._pd0.get_bottom_track()
    
        # mask by pg
        for i in range(bt_range.shape[0]):
            mask = self._pd0.get_leader_data(leader = 'BOTTOM TRACK', field = f'BEAM#{i+1} BT %GOOD')>0
            
            bt_range[i][~mask] = np.nan# ptools.rolling_spike_filter(bt_range[i] , window_size=spike_window, threshold_factor=spike_thresh)
    
        
        if any(~np.isnan(bt_range).flatten()):
            bt_range = np.repeat(bt_range[:, np.newaxis, :], self._pd0.config.number_of_cells, axis=1)
            bt_range[bt_range == 0] = 32675  # Presumed missing data code
            bin_centers = np.outer(self._pd0.geometry.get_bin_midpoints(), np.ones(self._pd0.n_ensembles))
            bin_centers = np.repeat(bin_centers[np.newaxis, :, :], self._pd0.config.number_of_beams, axis=0)
            mask = (bt_range - self._pd0.config.depth_cell_length / 100) > (bin_centers + cell_offset)
            self._pd0.mask.define_mask(mask=mask, name='bottom track', set_active=True)

         
    def _scalar_counts_to_absolute_backscatter(self,E,E_r,k_c,alpha,C,R,Tx_T, Tx_PL, P_DBW):
        """
        Absolute Backscatter Equation from Deines (Updated - Mullison 2017 TRDI Application Note FSA031)
    
        Parameters
        ----------
        E_r : float
            Measured RSSI amplitude in the absence of any signal (noise), in counts.
        C : float
            Constant combining several parameters specific to each instrument.
        k_c : float
            Factor to convert amplitude counts to decibels (dB).
        E : float
            Measured Returned Signal Strength Indicator (RSSI) amplitude, in counts.
        Tx_T : float
            Tranducer temperature in deg C.
        R : float
            Along-beam range to the measurement in meters
        alpha : float
            Acoustic absorption (dB/m). 
        Tx_PL : float
            Transmit pulse length in dBm.
        P_DBW : float
            Transmit pulse power in dBW.
    
        Returns
        -------
        tuple
            Tuple containing two elements:
            - Sv : float
                Apparent volume scattering strength.
            - StN : float
                True signal to noise ratio.
    
        Notes
        -----
        - The use of the backscatter equation should be limited to ranges beyond π/4 * Rayleigh Distance for the given instrument.
        - Rayleigh Distance is calculated as transmit pulse length * α / width, representing the distance at which the beam can be considered to have fully formed.
        - For further details, refer to the original documentation by Deines.
        - 𝑘_c is a factor used to convert the amplitude counts reported by the ADCP’s receive circuitry to decibels (dB).
        - 𝐸 is the measured Returned Signal Strength Indicator (RSSI) amplitude reported by the ADCP for each bin along each beam, in counts.
        - 𝐸_r is the measured RSSI amplitude seen by the ADCP in the absence of any signal (the noise), in counts, and which is constant for a given ADCP.
        """
        StN = (10**(k_c * E / 10) - 10**(k_c * E_r / 10)) / (10**(k_c * E_r / 10))
        L_DBM = 10 * np.log10(Tx_PL)
        #P_DBW = 10 * np.log10(Tx_Pw)
        Sv = C + 10 * np.log10((Tx_T + 273.16) * (R**2)) - L_DBM - P_DBW + 2 * alpha * R + 10 * np.log10((10**(0.1 * k_c * (E - E_r)) - 1))
    
        return Sv, StN
    
       
        
    def _scalar_water_absorption_coeff(self,T, S, z, f, pH):
        '''
        Calculate water absorption coefficient.
    
        Parameters
        ----------
        T : float
            Temperature in degrees Celsius.
        S : float
            Salinity in practical salinity units (psu).
        z : float
            Depth in meters.
        f : float
            Frequency in kHz.
        pH : float
            Acidity.
    
        Returns
        -------
        float
            Water absorption coefficient in dB/km.
        '''
        c = 1449.2 + 4.6 * T - 0.055 * T**2 + 0.00029 * T**3 + (0.0134 * T) * (S - 35) + 0.016 * z
        #c = 1412 + 3.21 * T + 1.19 * S + 0.0167 * z
    
        # Boric acid component
        A1 = (8.68 / c) * 10**(0.78 * pH - 5)
        P1 = 1
        f1 = 2.8 * ((S / 35)**0.5) * 10**(4 - (1245 / (273 + T)))
    
        # Magnesium sulphate component
        A2 = 21.44 * (S / c) * (1 + 0.025 * T)
        P2 = 1 - (1.37e-4) * z + (6.2e-9) * z**2
        f2 = (8.17 * 10**(8 - (1990 / (273 + T)))) / (1 + 0.0018 * (S - 35))
    
        if T <= 20:
            A3 = (4.937e-4) - (2.59e-5) * T + (9.11e-7) * T**2 - (1.5e-8) * T**3
        elif T > 20:
            A3 = (3.964e-4) - (1.146e-5) * T + (1.45e-7) * T**2 - (6.5e-8) * T**3
        P3 = 1 - (3.83e-5) * z + (4.9e-10) * (z**2)
    
        # Calculate water absorption coefficient
        alpha_w = (A1 * P1 * f1 * (f**2) / (f**2 + f1**2) + A2 * P2 * f2 * (f**2) / (f**2 + f2**2) + A3 * P3 * (f**2))
        
        # Convert absorption coefficient to dB/km
        alpha_w = (1 / 1000) * alpha_w
        
        return alpha_w
    
    
    def _scalar_sediment_absorption_coeff(self,ps, pw, d, SSC, T,S, f,z):
        '''
        Calculate sediment absorption coefficient.
    
        Parameters
        ----------
        ps : float
            Particle density in kg/m^3.
        pw : float
            Water density in kg/m^3.
        d : float
            Particle diameter in meters.
        SSC : float
            Suspended sediment concentration in kg/m^3.
        T : float
            Temperature in degrees Celsius.
        f : float
            Frequency in kHz .
    
        Returns
        -------
        float
            Sediment absorption coefficient.
        '''
        c = 1449.2 + 4.6 * T - 0.055 * T**2 + 0.00029 * T**3 + (0.0134 * T) * (S - 35) + 0.016 * z # speed of sound in water
        v = (40e-6) / (20 + T)  # Kinematic viscosity (m2/s)
        B = (np.pi * f / v) * 0.5
        delt = 0.5 * (1 + 9 / (B * d))
        sig = ps / pw
        s = 9 / (2 * B * d) * (1 + (2 / (B * d)))
        k = 2 * np.pi / c  # Wave number (Assumed, as it isn't defined in the paper)
    
        alpha_s = (k**4) * (d**3) / (96 * ps) + k * ((sig - 1)**2) / (2 * ps) + \
                  (s / (s**2 + (sig + delt)**2)) * (20 / np.log(10)) * SSC
    
        return alpha_s     

        

    def calculate_absolute_backscatter(self,**kwargs):
        """
        Convert numpy array of ensemble data of echo intensity to absolute backscatter then added to ensemble_data property of the WorkhorseADCP class.
    
        Optional Args:
            E_r
            k_c
            C
            alpha 
            P_dbw
     
        """
    
    
        E_r = 39 # noise floor 
        
        ## select C based on WB commmand (0 = 25%, 1 = 6.25%)
        WB = self._pd0.ensemble_data[0]['FIXED LEADER']['SYSTEM BANDWIDTH {WB}']
        if WB==0:
            C = -139.09 #for Workhorse 600, 25% 
        else:
            C = -149.14 # for Workhorse 600, 6%
        # Beam High Gain RSSI
        
        if hasattr(self._pd0,'PT3'):
            k_c = self._pd0.PT3.k_c
        else:
            k_c = {1: 0.3931,# beam 1
                    2: 0.4145,# beam 2
                    3: 0.416,# beam3
                    4: 0.4129}# beam4
        if self._pd0.ensemble_data[0]["SYSTEM CONFIGURATION"]["FREQUENCY"] == '300-kHz':
            alpha = 0.068 #nominal ocean value for a 600 kHz unit 
            P_dbw = 14 #battery supply power for Workhorse 300
            print('300 kHz Unit')
        elif self._pd0.ensemble_data[0]["SYSTEM CONFIGURATION"]["FREQUENCY"] == '600-kHz':
            alpha =  0.178 #nominal ocean value for a 600 kHz unit 
            P_dbw = 9 #battery supply power for Workhorse 600
            
        elif self._pd0.ensemble_data[0]["SYSTEM CONFIGURATION"]["FREQUENCY"] == '75-kHz':
            alpha =  0.027 #nominal ocean value for a 600 kHz unit 
            P_dbw = 27.3 #battery supply power for Workhorse 600
            
            
        # overwrite defaults with kwarg parameters 
        E_r = kwargs.pop('E_r',E_r) 
        C = kwargs.pop('C',C)
        k_c = kwargs.pop('k_c',k_c)
        alpha = kwargs.pop('alpha',alpha)
        P_dbw = kwargs.pop('P_dbw',P_dbw)
        
    
        #get other instrument data
        temperature = np.outer(self._pd0.get_sensor_temperature(),np.ones(self._pd0.config.number_of_cells)).T
        bin_distances = np.outer(self._pd0.geometry.get_bin_midpoints(),np.ones(self._pd0.n_ensembles))#/np.cos(20*np.pi/180)#/100
        transmit_pulse_lengths = np.outer(self._pd0.get_sensor_transmit_pulse_lengths(),np.ones(self._pd0.config.number_of_cells)).T#/100
        E = self._pd0.get_ensemble_array(field_name = 'ECHO INTENSITY') #echo intensity array 
        
        # initalize arrays  
        X = np.empty((self._pd0.config.number_of_beams,self._pd0.config.number_of_cells,self._pd0.n_ensembles))
        StN = np.empty((self._pd0.config.number_of_beams,self._pd0.config.number_of_cells,self._pd0.n_ensembles))
    
        for beam in range(self._pd0.config.number_of_beams):
            # StN[beam,:,:] = (10**(k_c[beam+1]*E[beam,:,:]/10) - 10**(k_c[beam+1]*E_r/10))/10**(k_c[beam+1]*E_r/10)
            # X[beam,:,:] = C + 10*np.log10((temperature + 273.16)*(bin_distances**2)) - 10*np.log10(transmit_pulse_lengths) - P_dbw + 2*alpha*bin_distances + 10*np.log10(10**(k_c[beam+1]*(E[beam,:,:] - E_r)/10)-1)
            
            sv,stn =self.counts_to_absolute_backscatter(E = E[beam],
                                                        E_r = E_r,
                                                        k_c= k_c[beam+1],
                                                        alpha = alpha,
                                                        C = C,
                                                        R = bin_distances,
                                                        Tx_T = temperature,
                                                        Tx_PL = transmit_pulse_lengths,
                                                        P_DBW = P_dbw)

            
            StN[beam] = stn
            X[beam] = sv
            
            
            #X[beam,:,:] = C + 10*np.log10((temperature*bin_distances**2)/(transmit_pulse_lengths*P_dbw)) + 2*alpha*bin_distances + k_c[beam+1]*(E[beam,:,:] - E_r)
        self.append_to_ensembles(X,'ABSOLUTE BACKSCATTER')
        self.append_to_ensembles(StN,'SIGNAL TO NOISE RATIO')   
        
        
        
        
    def append_to_ensembles(self,X,title,nan_value = 32768):
        """
        Format numpy array of ensemble data into a list then add to ensemble_data property of the WorkhorseADCP class.
        Input array must have dimensions of (n_beams,nbins,n_ensemles). In a typical use case, ensemble data is manipulated in 
        array format, then appended to the ensemble_data property and written to a PD0 file. 
        Args:
            X: numpy array with dimensions (n_bins,n_ensembles,n_beams)
            title: (string) title for the formatted data when appended to the ensemble_data property of the WorkhorseADCP class object. 
            nan_value: (int) value to use in place of nan. 32768 is default. 
        """
        self.ensemble_fields.append(title) # update the list of ensemble field names
        for e in range(self._pd0.n_ensembles):
            ensemble_data = [] # data in the current ensemble
            for b in range(self._pd0.config.number_of_cells):
                bin_data = [] # data in the current bin
                for bm in range(self._pd0.config.number_of_beams):
                    
                    val = X[bm,b,e]
                    #bin_data.append(int(val))
                    try:
                        bin_data.append(int(val))
                    except:
                        bin_data.append(nan_value)
                        
                        
                ensemble_data.append(bin_data)
            self._pd0.ensemble_data[e][title] = ensemble_data  