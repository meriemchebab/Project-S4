from PySide6.QtCore import QObject
import numpy as np 
from scipy.signal import savgol_filter

class Model():
    def __init__(self, parent =None):
        
        self.h_plane2D = None
        self.e_plane2D = None
        self.h_plane3D = None
        self.e_plane3D = None
        self.h_plane = None
        self.e_plane = None
        self.maxH = None
        self.maxE = None

        
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
        self.e_plane2D= np.array(self.e_plane)
        self.h_plane2D= np.array(self.h_plane)
        self.h_plane3D= np.array(self.h_plane)
        self.e_plane3D= np.array(self.e_plane)
        # this 2 will be used in the smooth and will not change at all
        self.e_plane = np.array(self.e_plane)
        self.h_plane = np.array(self.h_plane)
        # set each data to the figure type 
    def normalize(self, mode):
        if mode == "2D" and self.h_plane2D is not None and self.e_plane2D is not None:
            self.h_plane2D = self.h_plane2D - np.max(self.h_plane2D)
            self.e_plane2D = self.e_plane2D - np.max(self.e_plane2D)

        elif mode == "3D" and self.h_plane3D is not None and self.e_plane3D is not None:
            self.h_plane3D = self.h_plane3D - np.max(self.h_plane3D)
            self.e_plane3D = self.e_plane3D - np.max(self.e_plane3D)
    def denormalize(self,mode):
        self.maxH = np.max(self.h_plane)
        self.maxE = np.max(self.e_plane)
        if mode == "2D" and self.h_plane2D is not None and self.e_plane2D is not None:
            self.h_plane2D = self.h_plane2D + self.maxH
            self.e_plane2D = self.e_plane2D + self.maxE

        elif mode == "3D" and self.h_plane3D is not None and self.e_plane3D is not None:
            self.h_plane3D = self.h_plane3D + self.maxH
            self.e_plane3D = self.e_plane3D + self.maxE


    def smooth2D(self, number):
        if self.e_plane is not None and self.h_plane is not None:
            if number % 2 == 0:
                number += 1

            # Always smooth from original clean data
            
            
                smoothed_h = savgol_filter(self.h_plane, window_length=number, polyorder=2)
                smoothed_e = savgol_filter(self.e_plane, window_length=number, polyorder=2)
            
                self.h_plane2D = smoothed_h
                self.e_plane2D = smoothed_e
                # always normlize after smmohting
                self.normalize("2D")
            
    def smooth3D(self,bool):
        if self.e_plane is not None and self.h_plane is not None and bool:            
            self.h_plane3D= savgol_filter(self.h_plane, window_length=11, polyorder=2)
            self.e_plane3D= savgol_filter(self.e_plane, window_length=11, polyorder=2)
            self.normalize("3D")
        else : 
            self.h_plane3D = self.h_plane
            self.e_plane3D = self.e_plane

    def data_3D(self):
        size = len(self.h_plane)
        theta = np.linspace(0, 2 * np.pi,size)
        phi = np.linspace(0, np.pi,size )
        theta, phi = np.meshgrid(theta, phi)
        
        
        # Fake 3D radial values by averaging E & H
        r = (np.outer(self.h_plane3D, np.ones_like(self.e_plane3D)) + np.outer(np.ones_like(self.h_plane3D),self.e_plane3D )) / 2

        # Convert spherical to cartesian
        X = r * np.sin(phi) * np.cos(theta)
        Y = r * np.sin(phi) * np.sin(theta)
        Z = r * np.cos(phi)
        return X,Y,Z
    

