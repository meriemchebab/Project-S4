
import sys
import numpy as np 
from scipy.signal import savgol_filter

class Model():
    def __init__(self):
        self.h_plane = None
        self.e_plane = None
        self.N_hplane = None
        self.N_eplane = None
        self.smooth_h = None
        self.smooth_e = None
        self.phi_h = None
        self.phi_e = None
        self.X = None
        self.Y = None
        self.Z = None

        
    def read_file(self,file_path):
        
        self.h_plane = []
        self.e_plane = []

        reading_started = False  # We haven't started reading numbers yet
        reading_h_plane = True   # When we start, we assume it's H-plane

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Clean whitespace
                
                if not line:
                    continue  # Skip empty lines

                try:
                    value = float(line)
                    reading_started = True  # First number seen → real data starts now

                    if reading_h_plane:
                        self.h_plane.append(value)
                    else:
                        self.e_plane.append(value)

                except ValueError:
                    # Failed to parse float → it's metadata
                    if reading_started:
                        # If reading already started and now metadata → switch to E-plane
                        reading_h_plane = False
                    # Else: still skipping initial metadata
                    continue
        # give me the data clean in an array for the use in plot        
        self.e_plane=np.array(self.e_plane)
        self.h_plane= np.array(self.h_plane)
    def normelize(self):
        if self.e_plane is not None and self.h_plane is not None:

            
            self.N_eplane = self.e_plane - np.max(self.e_plane)
            self.N_hplane = self.h_plane - np.max(self.h_plane)


    def smooth(self,number):

        if self.e_plane is not None and self.h_plane is not None:

            if number % 2 == 0:
                number += 1
            self.smooth_h = savgol_filter(self.h_plane, window_length= number, polyorder=2)
            self.smooth_e= savgol_filter(self.e_plane, window_length= number, polyorder=2)
    def data_2D(self):
        self.phi_h = np.radians(np.arange(len(self.h_plane)))  
        self.phi_e = np.radians(np.arange(len(self.e_plane)))
    def data_3D(self):
        size = len(self.h_plane)//2
        theta = np.linspace(0, 2 * np.pi,size)
        phi = np.linspace(0, np.pi,size )
        theta, phi = np.meshgrid(theta, phi)

        # Fake 3D radial values by averaging E & H
        r = (np.outer(self.h_plane, np.ones_like(self.e_plane)) + np.outer(np.ones_like(self.h_plane),self.e_plane )) / 2

        # Convert spherical to cartesian
        self.X = r * np.sin(phi) * np.cos(theta)
        self.Y = r * np.sin(phi) * np.sin(theta)
        self.Z = r * np.cos(phi)