from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from PySide6.QtWidgets import (QPushButton, QMainWindow, 
                              QWidget, QVBoxLayout, QFileDialog, 
                              QRadioButton, QHBoxLayout,QSlider,QColorDialog)

from PySide6.QtCore import Qt
import numpy as np

# this is the figure we will draw on there is tow kinds 2D and 3D so i subclassed it  
class Myfig(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=[12, 8])
        super().__init__(self.fig)
        if parent:
            self.setParent(parent)
        # Initialize axes as None (we'll create them when needed)
class Fig2D(Myfig):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ax1 = None 
        self.ax2 = None 
        
    def update_ax2(self, mode):
        if mode == 1:
            self.ax1 = self.fig.add_subplot(121, polar=True)
            self.ax2 = self.fig.add_subplot(122, polar=True)
        else :
            self.ax1 = self.fig.add_subplot(111, polar=True)
class Fig3D(Myfig):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ax3 = None
    def setupAX3(self):
        self.ax3 = self.fig.add_subplot(111, projection='3d')
    
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        main = QWidget()
        
        self.fig2D = Fig2D(self)
        self.fig3D = Fig3D(self)
        self.h_color = 'b'
        self.e_color = 'red'
        self.readButton = QPushButton("open", self)
        
        self.normal = QRadioButton("normelize", self)
        
        self.toolbar = NavigationToolbar(self.fig2D, self)
        self.slider = QSlider()
        self.slider.setMaximum(6)
        self.slider.setMinimum(1)
        self.slider.setOrientation(Qt.Horizontal) 

        Button_row = QHBoxLayout()
        Button_row.addWidget(self.readButton)
        Button_row.addWidget(self.plot2D_same)
        Button_row.addWidget(self.plot2D_split)
        Button_row.addWidget(self.normal)

        layout = QVBoxLayout()
        layout.addLayout(Button_row)
        layout.addWidget(self.slider)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.fig2D, stretch=1)
        main.setLayout(layout)
        self.setCentralWidget(main)


    

    def pick_color_for(self, plane='h'):
        color = QColorDialog.getColor()

        if color.isValid():
            hex_color = color.name()  # '#rrggbb'
            if plane == 'h':
                self.h_color = hex_color
            elif plane == 'e':
                self.e_color = hex_color
    def open_file(self):
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setNameFilter("atn files (*.atn);;Text Files (*.txt)")
            if dialog.exec():
                 file_name = dialog.selectedFiles()[0]
                 return file_name
    def plot_2D(self ,h,e,mode):

        if not e or not h :
            raise ValueError
        else:
            # calculate the angles 
            theta_h = np.radians(np.arange(len(h)))  
            theta_e = np.radians(np.arange(len(e)))
            if mode == 1: # plot in the same place
                self.fig2D.ax1.clear()
                self.fig2D.ax1.plot(theta_h,e, label='E-plane', color=self.h_color)
                self.fig2D.ax1.plot(theta_e, h, label='H-plane', color=self.e_color)
                self.fig2D.ax1.set_title("H_palne and E_plane ")
                self.fig2D.ax1.legend()
                self.fig2D.ax1.draw()
                self.toolbar.push_current()   
            #maybe color change here
            else :
                self.fig2D.ax1.clear()
                self.fig2D.ax2.clear()
                self.fig2D.ax1.plot(theta_h, h, label='H-plane', color=self.h_color)
                self.fig2D.ax1.set_title('H-plane Pattern (dB)')
                
                
                self.fig2D.ax1.legend()

                # Plot E-plane
                self.fig2D.ax2.plot(theta_e, e, label='E-plane', color=self.e_color)
                self.fig2D.ax2.set_title('E-plane Pattern (dB)')
                self.fig2D.ax2.legend()
                self.fig2D.ax2.set_theta_direction(-1)
                # Redraw the canvas
                self.fig2D.draw()
                
                # Push the current view to the navigation stack
                self.toolbar.push_current()    
        return
    def plot_3D(self, x,y ,z):
        surf = self.fig3D.ax3.plot_surface(x, y, z, cmap='viridis', edgecolor='none', alpha=0.8)
        self.fig3D.colorbar(surf, ax=self.fig3D.ax3, shrink=0.5, label='Radiation Intensity (linear)')

        self.fig3D.ax3.set_title('3D Antenna Radiation Pattern (Matplotlib)')
        self.fig3D.ax3.set_xlabel('X')
        self.fig3D.ax3.set_ylabel('Y')
        self.fig3D.ax3.set_zlabel('Z')
        self.fig3D.ax3.view_init(elev=30, azim=45)   
                    






        

                   

        
            
        