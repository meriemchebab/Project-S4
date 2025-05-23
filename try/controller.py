from logic import Model
from UI_file import Window
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
import json
import numpy as np
class Controler(QObject):
    def __init__(self  ,  parent = None):
        super().__init__(parent)
        self.model=Model(self)
        self.ui = Window()  # Remove self as argument
        
        self.listHistory = {
                 "h_plane2D":[],
                "e_plane2D":[],
                "h_plane3D":[],
                "e_plane3D":[],
                "e_color":[],
                "h_color" : [],
                "3d_color":[],
                "show_lobes": []
            }
        self.index = -1
        self.i = -1
        # the signals and slots 
        
        self.ui.view.import_button.clicked.connect(self.read)
        self.ui.view.plot_3d_button.clicked.connect(self.polar_3D)
        self.ui.view.display_mode_menu.actions()[0].triggered.connect(self.polar_2D_split)
        self.ui.view.display_mode_menu.actions()[1].triggered.connect(self.polar_2D_same)

        self.ui.view.offset_button.clicked.connect(self.normal)

       
        self.ui.view.zoom_in_button1.clicked.connect(self.ui.fig2D.zoom_in)
        self.ui.view.zoom_out_button1.clicked.connect(self.ui.fig2D.zoom_out)
        self.ui.view.zoom_in_button2.clicked.connect(self.ui.fig3D.zoom_in)
        self.ui.view.zoom_out_button2.clicked.connect(self.ui.fig3D.zoom_out)
        self.ui.view.color_button3D.clicked.connect(self.color_3D)
        self.ui.view.color_button1.clicked.connect(self.color_2D)

        self.ui.view.back_button1.clicked.connect(self.GoBack)
        self.ui.view.next_button1.clicked.connect(self.GoForth)
        self.ui.view.back_button2.clicked.connect(self.GoBack)
        self.ui.view.next_button2.clicked.connect(self.GoForth)

        # In your controller __init__ after self.ui.view is created:
        self.ui.view.smoothness_slider1.valueChanged.connect(self.smooth_2D)
        self.ui.view.smoothness_slider2.valueChanged.connect(self.smooth_3D)
        #to show the highlight 
        self.ui.view.highlight_lobes_button.toggled.connect(self.toggle_lobes_highlighting)


#self.smoothness_slider1.valueChanged.connect(controller.smooth_2D)

#self.smoothness_slider2.valueChanged.connect(controller.smooth_3D)

#reading a file


    def toggle_lobes_highlighting(self, checked):
        try:
            self.ui.fig2D.show_lobes = checked
            self.listHistory["show_lobes"].append(checked)  # Update history
            self.limitListSize()
            if self.ui.fig2D.h_data is not None and self.ui.fig2D.e_data is not None:
                self.ui.fig2D.plot_2D(self.ui.fig2D.h_data, self.ui.fig2D.e_data)
                self.ui.toolbar1.push_current()
            else:
                self.ui.view.statusbar.showMessage("No data to highlight. Please import data first.")
        except Exception as e:
            self.ui.view.statusbar.showMessage(f"Error highlighting lobes: {str(e)}")
            print(f"Error in toggle_lobes_highlighting: {e}")

    def read(self):
            
            file_name = self.ui.open_file()
            self.model.read_file(file_name)
            
            # this is the history i take a reference of the data so i can go back to it 
            Hdata2= self.model.h_plane2D.copy()
            Edata2 = self.model.e_plane2D.copy()
            Hdata3 = self.model.h_plane3D.copy()
            Edata3 = self.model.e_plane3D.copy()
            color2e =self.ui.fig2D.color_e
            color2h =self.ui.fig2D.color_h
            color3D = self.ui.fig3D.cmap
            show_lobes = self.ui.fig2D.show_lobes

            self.listHistory["h_plane2D"].append(Hdata2)
            self.listHistory["e_plane2D"].append(Edata2)
            self.listHistory["h_plane3D"].append(Hdata3)
            self.listHistory["e_plane3D"].append(Edata3)
            self.listHistory["e_color"].append(color2e)
            self.listHistory["h_color"].append(color2h)
            self.listHistory["3d_color"].append(color3D)
            self.listHistory["show_lobes"].append(show_lobes)
            
            self.index +=1
            self.limitListSize()
            # now update the slider max , if we read 72 value or 360 it will change
            self.update_smooth_slider()
            # when the previos button clik
            # go for this
    def can_goBack(self):
            if self.index > 0 :
                  return True
            else :
                return False

    def can_goForth(self):
          return self.index < len(self.listHistory["h_plane2D"])-1
             
            #index = length(self.listHistory["h_plane"]) - 1
    def GoBack(self):
          if self.can_goBack():
            self.index -=1
            self.model.h_plane2D = self.listHistory["h_plane2D"][self.index]
            self.model.e_plane2D = self.listHistory["e_plane2D"][self.index]
            self.model.h_plane3D = self.listHistory["h_plane3D"][self.index]
            self.model.e_plane3D = self.listHistory["e_plane3D"][self.index]
            self.ui.fig2D.color_h = self.listHistory["h_color"][self.index]
            self.ui.fig2D.color_e = self.listHistory["e_color"][self.index]
            self.ui.fig3D.cmap = self.listHistory["3d_color"][self.index]
            self.ui.fig2D.show_lobes = self.listHistory["show_lobes"][self.index]
            self.update_smooth_slider()
            
    def GoForth(self):
         if  self.can_goForth():
            self.index +=1
            self.model.h_plane2D = self.listHistory["h_plane2D"][self.index]
            self.model.e_plane2D = self.listHistory["e_plane2D"][self.index]
            self.model.h_plane3D = self.listHistory["h_plane3D"][self.index]
            self.model.e_plane3D = self.listHistory["e_plane3D"][self.index]
            self.ui.fig2D.color_h = self.listHistory["h_color"][self.index]
            self.ui.fig2D.color_e = self.listHistory["e_color"][self.index]
            self.ui.fig3D.cmap = self.listHistory["3d_color"][self.index]
            self.ui.fig2D.show_lobes = self.listHistory["show_lobes"][self.index]
            self.update_smooth_slider()          
    def limitListSize(self):
         i = len(self.listHistory["h_plane2D"]) - 1
         if i>6 :
            self.listHistory["h_plane2D"].pop(0) 
            self.listHistory["e_plane2D"].pop(0) 
            self.listHistory["h_plane3D"].pop(0) 
            self.listHistory["e_plane3D"].pop(0) 
            self.listHistory["h_color"].pop(0) 
            self.listHistory["e_color"].pop(0) 
            self.listHistory["3d_color"].pop(0) 
                     
    def polar_2D_same(self):
         self.ui.fig2D.toggle_mode(False)
         self.ui.fig2D.plot_2D(self.model.h_plane2D,self.model.e_plane2D)
         self.ui.toolbar1.push_current()
    def polar_2D_split(self):
        self.ui.fig2D.toggle_mode(True)
        self.ui.fig2D.plot_2D(self.model.h_plane2D,self.model.e_plane2D)
        self.ui.toolbar1.push_current()
        
    
        
    def polar_3D(self):
      # make new figure
        
        X, Y, Z = self.model.data_3D()
        self.ui.fig3D.plot_surface(X, Y, Z)
        self.ui.toolbar2.push_current()
            
    def normal(self):
        if self.ui.view.offset_button.isChecked():

            self.model.normalize('2D')
            self.model.normalize('3D')                
            self.ui.fig2D.plot_2D(self.model.h_plane2D,self.model.e_plane2D)
            self.ui.toolbar2.push_current()
        else :
            self.model.denormalize('2D')
            self.model.denormalize('3D')
            self.ui.fig2D.plot_2D(self.model.h_plane2D,self.model.e_plane2D)
            self.ui.toolbar2.push_current()


    def smooth_3D(self ,number):
        self.model.smooth(number,"3D")
        X,Y,Z = self.model.data_3D()
        self.ui.fig3D.plot_surface(X, Y, Z)
        self.ui.toolbar2.push_current()
    def smooth_2D(self ,number):
        self.model.smooth(number,"2D")
        self.ui.fig2D.plot_2D(self.model.h_plane2D,self.model.e_plane2D) 
        self.ui.toolbar2.push_current()
        # you have to set the max window for the slider
    def update_smooth_slider(self):
    # Assume self.model.h_plane is your current data array
        data_len = len(self.model.h_plane)
        max_window = max(5, data_len // 5)
        if max_window % 2 == 0:
            max_window -= 1
        self.ui.view.smoothness_slider1.setRange(5, max_window)
        self.ui.view.smoothness_slider2.setRange(5, max_window)
    def color_2D(self):
         self.ui.pick_color_for()
         self.ui.fig2D.plot_2D(self.model.h_plane2D,self.model.e_plane2D)
         self.ui.toolbar1.push_current() 
    def color_3D(self):
        COLORMAPS_3D = (
            "viridis",
            "plasma",
            "inferno",
            "magma",
            "cividis",
            "jet",
            "coolwarm",
            "turbo",
            "rainbow",
            "hsv"
        )
        self.i = (self.i + 1) % len(COLORMAPS_3D)
        self.ui.fig3D.cmap = COLORMAPS_3D[self.i]
        X, Y, Z = self.model.data_3D()
        self.ui.fig3D.plot_surface(X, Y, Z)
        self.ui.toolbar2.push_current()
        
     

    def load_project(self):
         # read from a json file        
        file_path = self.ui.file_history("open")
        
        
        
        with open(file_path, 'r') as f:
            loaded_history = json.load(f)
        # Convert lists back to numpy arrays where appropriate
        
        for k, v in loaded_history.items():
            self.listHistory[k] = []
            for item in v:
                if k.endswith('plane2D') or k.endswith('plane3D'):
                    self.listHistory[k].append(np.array(item))
                else:
                    self.listHistory[k].append(item)
        self.index = len(self.listHistory["h_plane2D"]) - 1
        # Restore the latest state to the model/UI
        try:
            QMessageBox.information(self, "Success", f"Project loaded from {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load project: {e}")
        if self.index >= 0:
            self.model.h_plane2D = self.listHistory["h_plane2D"][self.index]
            self.model.e_plane2D = self.listHistory["e_plane2D"][self.index]
            self.model.h_plane3D = self.listHistory["h_plane3D"][self.index]
            self.model.e_plane3D = self.listHistory["e_plane3D"][self.index]
            self.ui.fig2D.color_h = self.listHistory["h_color"][self.index]
            self.ui.fig2D.color_e = self.listHistory["e_color"][self.index]
            self.ui.fig3D.cmap = self.listHistory["3d_color"][self.index]
            # Redraw plots
        self.update_smooth_slider()       
            
    def save_project(self):
        file_path = self.ui.file_history("save")
            # Convert all numpy arrays to lists for JSON serialization
        serializable_history = {}
        for k, v in self.listHistory.items():
            serializable_history[k] = []
            for item in v:
                try:
                    serializable_history[k].append(item.tolist())
                except AttributeError:
                    serializable_history[k].append(item)
        try:
            with open(file_path, 'w') as f:
                json.dump(serializable_history, f)
            QMessageBox.information(self.ui, "Success", f"Project saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", f"Failed to save project: {e}")