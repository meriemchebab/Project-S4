from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


from PySide6.QtWidgets import ( QMainWindow, 
                                QFileDialog,QMessageBox, 
                              QColorDialog)

from widgets import Ui_Window
import numpy as np



from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import numpy as np

class Fig3D(FigureCanvasQTAgg):
    def __init__(self, parent=None, figsize=(8, 6)):
        # 1. Create and pass the Figure into the FigureCanvas
        fig = Figure(figsize=figsize)
        super().__init__(fig)
        if parent:
            self.setParent(parent)

        # 2. Create the 3D axes exactly once
        self.ax3 = self.figure.add_subplot(111, projection='3d')
        
        # 3. Placeholder for the colorbar so we can remove it later
        self._cbar = None

        # Default colormap
        self.cmap = 'plasma'

    def plot_surface(self, X, Y, Z):
        # 4a. Clear just the axes (not the entire figure)
        self.ax3.clear()
        # 4b. If there was a previous colorbar, remove it
        if self._cbar:
            self._cbar.remove()
            self._cbar = None

        # 5. Plot and add a single colorbar
        surf = self.ax3.plot_surface(
            X, Y, Z,
            cmap=self.cmap,
            edgecolor='none',
            alpha=0.8
        )
        self._cbar = self.figure.colorbar(
            surf, ax=self.ax3, shrink=0.5,
            label='Radiation Intensity (linear)'
        )

        # 6. Restore labels and view
        self.ax3.set_title('3D Antenna Radiation Pattern')
        self.ax3.set_xlabel('X')
        self.ax3.set_ylabel('Y')
        self.ax3.set_zlabel('Z')
        self.ax3.view_init(elev=30, azim=45)

        # 7. Trigger a redraw
        self.draw()

    def zoom_in(self, factor=0.8):
    # Remove the unnecessary check or make it meaningful
        min_width = 1e-3
        for getter, setter in [
            (self.ax3.get_xlim, self.ax3.set_xlim),
            (self.ax3.get_ylim, self.ax3.set_ylim), 
            (self.ax3.get_zlim, self.ax3.set_zlim),
        ]:
            try:
                lo, hi = getter()
                center = 0.5*(lo+hi)
                half = max((hi-lo)*factor/2, min_width)
                setter((center-half, center+half))
            except Exception as e:
                print(f"Error in zoom_in: {e}")
                continue
        self.draw()

    def zoom_out(self, factor=1.25):
        max_width = 1e6
        for getter, setter in [
            (self.ax3.get_xlim, self.ax3.set_xlim),
            (self.ax3.get_ylim, self.ax3.set_ylim),
            (self.ax3.get_zlim, self.ax3.set_zlim),
        ]:
            try:
                lo, hi = getter()
                center = 0.5*(lo+hi)
                half = min((hi-lo)*factor/2, max_width)
                setter((center-half, center+half))
            except Exception as e:
                print(f"Error in zoom_out: {e}")
                continue
        self.draw()  # True → split; False → overlaid
class Fig2D(FigureCanvasQTAgg):
    def __init__(self, parent=None, figsize=(12, 8)):
        # 1. Create and pass the Figure into the FigureCanvas
        fig = Figure(figsize=figsize)
        super().__init__(fig)
        if parent:
            self.setParent(parent)
        self.color_h ="blue"
        self.color_e ="red"
        self.ax1 = self.figure.add_subplot(121, polar=True)
        self.ax2 = self.figure.add_subplot(122, polar=True)
        self.use_two_plots = True 
    def toggle_mode(self, two_plots: bool):
        """Switch between single- and dual-axis modes."""
        self.use_two_plots = two_plots
        
        

    def plot_2D(self,h,e):
        # Clear whatever axes you’re about to use
        self.ax1.clear()
        self.ax2.clear()
        theta_h = np.radians(np.arange(len(h)))  
        theta_e = np.radians(np.arange(len(e)))
        if self.use_two_plots:
            
            # plot H on left, E on right
            self.ax1.plot(theta_h, h, color=self.color_h, label='H-plane')
            self.ax1.set_title('H-plane')
            self.ax2.set_theta_direction(-1)
            self.ax1.legend()

            self.ax2.plot(theta_e,e,color =  self.color_e, label='E-plane')
            
            self.ax2.set_title(" E_plane ")
                
            self.ax2.legend()

        else:
            # overlay
            self.ax1.plot(theta_h, h, color=self.color_h, label='H-plane')
            self.ax1.plot(theta_e, e, color=self.color_e, label='E-plane')
            self.ax1.set_title('H & E overlay')
            self.ax1.legend()
            
            self.ax2.plot(theta_h, h, color=self.color_h, label='H-plane')
            self.ax2.plot(theta_e, e, color=self.color_e, label='E-plane')
            self.ax2.set_title('H & E rotated')
            self.ax2.set_theta_direction(1)
            self.ax2.legend()
            
        self.draw()

    def zoom_in(self, factor=0.8):
        min_ylim = 1e-3
        max_ylim = 1e6
        
        # Always zoom both axes since both are visible
        for ax in [self.ax1, self.ax2]:
            if ax is not None:
                try:
                    rmin, rmax = ax.get_ylim()
                    new_rmax = max(min(rmax * factor, max_ylim), min_ylim)
                    if new_rmax > min_ylim:
                        ax.set_ylim(rmin, new_rmax)
                except Exception as e:
                    print(f"Error zooming axis: {e}")
                    continue
        self.draw()

    def zoom_out(self, factor=1.25):
        min_ylim = 1e-3
        max_ylim = 1e6
        
        # Always zoom both axes since both are visible
        for ax in [self.ax1, self.ax2]:
            if ax is not None:
                try:
                    rmin, rmax = ax.get_ylim()
                    new_rmax = max(min(rmax * factor, max_ylim), min_ylim)
                    if new_rmax > min_ylim:
                        ax.set_ylim(rmin, new_rmax)
                except Exception as e:
                    print(f"Error zooming axis: {e}")
                    continue
        self.draw()
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = Ui_Window()
        self.view.setupUi(self)

        # Create your figures
        self.fig2D = Fig2D(self)
        self.fig3D = Fig3D(self)

        # Create toolbars
        self.toolbar1 = NavigationToolbar(self.fig2D, self)
        self.toolbar2 = NavigationToolbar(self.fig3D, self)

        # Add FigureCanvas and NavigationToolbar to the view's layouts
        self.view.tab1_canvas_layout.addWidget(self.toolbar1)
        self.view.tab1_canvas_layout.addWidget(self.fig2D)
        self.view.tab2_canvas_layout.addWidget(self.toolbar2)
        self.view.tab2_canvas_layout.addWidget(self.fig3D)

   
# pick a color 
    def pick_color_for(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Select Plane")
        msg.setText("Which plane's color do you want to change?")
        h_button = msg.addButton("H-plane", QMessageBox.AcceptRole)
        e_button = msg.addButton("E-plane", QMessageBox.AcceptRole)
        msg.exec()

        if msg.clickedButton() == h_button:
            plane = 'h'
        elif msg.clickedButton() == e_button:
            plane = 'e'
        else:
            return  # User closed dialog

        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            if plane == 'h':
                self.fig2D.color_h = hex_color
            elif plane == 'e':
                self.fig2D.color_e = hex_color
    def open_file(self):
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setNameFilter("atn files (*.atn);;Text Files (*.txt)")
            if dialog.exec():
                 file_name = dialog.selectedFiles()[0]
                 return file_name
    def file_history(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.setDefaultSuffix("json")
        if file_dialog.exec():
            return file_dialog.selectedFiles()[0]




















