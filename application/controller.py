from logic import Model
from UI_file import Window
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
import json
import numpy as np
import os
import plotly.graph_objects as go
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

        self.ui.view.offset_button.toggled.connect(self.normal)

       
        
        self.ui.view.zoom_in_button2.clicked.connect(self.ui.fig3D.zoom_in)
        self.ui.view.zoom_out_button2.clicked.connect(self.ui.fig3D.zoom_out)
        
        self.ui.view.color_button1.clicked.connect(self.color_2D)

        self.ui.view.back_button1.clicked.connect(self.GoBack)
        self.ui.view.next_button1.clicked.connect(self.GoForth)
        self.ui.view.back_button2.clicked.connect(self.GoBack)
        self.ui.view.next_button2.clicked.connect(self.GoForth)
        self.ui.view.save_button.clicked.connect(self.save_project)
        # In your controller __init__ after self.ui.view is created:
        self.ui.view.smoothness_slider1.valueChanged.connect(self.smooth_2D)
        self.ui.view.smooth_button.toggled.connect(self.smooth_3D)
        self.ui.view.online_view_button.clicked.connect(self.load_project)

        #to show the highlight 
        self.ui.view.highlight_lobes_button.toggled.connect(self.toggle_lobes_highlighting)


#reading a file

    def toggle_lobes_highlighting(self, checked):
        try:
            self.ui.fig2D.show_lobes = checked
            self.listHistory["show_lobes"].append(checked)
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
        try:
            file_name = self.ui.open_file()
            if not file_name:  # User cancelled file dialog
                return
                
            self.model.read_file(file_name)
            
            # Create history entry
            Hdata2 = self.model.h_plane2D.copy()
            Edata2 = self.model.e_plane2D.copy()
            Hdata3 = self.model.h_plane3D.copy()
            Edata3 = self.model.e_plane3D.copy()
            color2e = self.ui.fig2D.color_e
            color2h = self.ui.fig2D.color_h
            

            if Hdata2 is None or Edata2 is None:
                raise ValueError("Failed to load valid 2D data from file")
            
            self.listHistory["h_plane2D"].append(Hdata2)
            self.listHistory["e_plane2D"].append(Edata2)
            self.listHistory["h_plane3D"].append(Hdata3)
            self.listHistory["e_plane3D"].append(Edata3)
            self.listHistory["e_color"].append(color2e)
            self.listHistory["h_color"].append(color2h)
            
            
            self.index += 1
            self.limitListSize()

            
            
            
        except FileNotFoundError:
            QMessageBox.critical(self.ui, "File Error", "The selected file could not be found.")
        except PermissionError:
            QMessageBox.critical(self.ui, "Permission Error", "You don't have permission to read this file.")
        except Exception as e:
            QMessageBox.critical(self.ui, "Import Error", f"Failed to import file:\n{str(e)}")
    def can_goBack(self):
            if self.index > 0 :
                  return True
            else :
                return False

    def can_goForth(self):
          return self.index < len(self.listHistory["h_plane2D"])-1
    def GoBack(self):
        try:
            if not self.can_goBack():
                QMessageBox.warning(self.ui, "Navigation", "Already at the first state in history.")
                return
                
            self.index -= 1
            
            # Validate history data exists
            if (self.index >= len(self.listHistory["h_plane2D"]) or 
                self.index >= len(self.listHistory["e_plane2D"])):
                QMessageBox.critical(self.ui, "History Error", "History data is corrupted.")
                self.index += 1  # Revert index
                return
                
            self.model.h_plane2D = self.listHistory["h_plane2D"][self.index]
            self.model.e_plane2D = self.listHistory["e_plane2D"][self.index]
            self.model.h_plane3D = self.listHistory["h_plane3D"][self.index]
            self.model.e_plane3D = self.listHistory["e_plane3D"][self.index]
            self.ui.fig2D.color_h = self.listHistory["h_color"][self.index]
            self.ui.fig2D.color_e = self.listHistory["e_color"][self.index]
            
            self.ui.fig2D.plot_2D(self.model.h_plane2D, self.model.e_plane2D)
            self.ui.toolbar1.push_current()  # Preserve 2D plot axes
            
        except IndexError:
            QMessageBox.critical(self.ui, "History Error", "Cannot navigate back - history index out of range.")
            self.index = max(0, self.index)  # Reset to valid index
        except Exception as e:
            QMessageBox.critical(self.ui, "Navigation Error", f"Failed to go back:\n{str(e)}")

    def GoForth(self):
        try:
            if not self.can_goForth():
                QMessageBox.warning(self.ui, "Navigation", "Already at the latest state in history.")
                return
                
            self.index += 1
            
            # Validate history data exists
            if (self.index >= len(self.listHistory["h_plane2D"]) or 
                self.index >= len(self.listHistory["e_plane2D"])):
                QMessageBox.critical(self.ui, "History Error", "History data is corrupted.")
                self.index -= 1  # Revert index
                return
                
            self.model.h_plane2D = self.listHistory["h_plane2D"][self.index]
            self.model.e_plane2D = self.listHistory["e_plane2D"][self.index]
            self.model.h_plane3D = self.listHistory["h_plane3D"][self.index]
            self.model.e_plane3D = self.listHistory["e_plane3D"][self.index]
            self.ui.fig2D.color_h = self.listHistory["h_color"][self.index]
            self.ui.fig2D.color_e = self.listHistory["e_color"][self.index]
            
            self.ui.fig2D.plot_2D(self.model.h_plane2D, self.model.e_plane2D)
            self.ui.toolbar1.push_current()  # Preserve 2D plot axes
            
        except IndexError:
            QMessageBox.critical(self.ui, "History Error", "Cannot navigate forward - history index out of range.")
            self.index = min(len(self.listHistory["h_plane2D"]) - 1, self.index)  # Reset to valid index
        except Exception as e:
            QMessageBox.critical(self.ui, "Navigation Error", f"Failed to go forward:\n{str(e)}")
    def limitListSize(self):
        i = len(self.listHistory["h_plane2D"]) - 1
        if i>6 :
            self.listHistory["h_plane2D"].pop(0) 
            self.listHistory["e_plane2D"].pop(0) 
            self.listHistory["h_plane3D"].pop(0) 
            self.listHistory["e_plane3D"].pop(0) 
            self.listHistory["h_color"].pop(0) 
            self.listHistory["e_color"].pop(0) 
           
    def normal(self):
        try:
            if self.ui.view.offset_button.isChecked():
                self.model.normalize('2D')
                self.model.normalize('3D')
                operation = "normalization"
            else:
                self.model.denormalize('2D')
                self.model.denormalize('3D')
                operation = "denormalization"
            
            # Update both 2D 
            self.ui.fig2D.plot_2D(self.model.h_plane2D, self.model.e_plane2D)
            
            
           
            
            
        except AttributeError as e:
            QMessageBox.critical(self.ui, "Data Error", f"Model data not available for {operation}:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self.ui, "Processing Error", f"Failed to apply {operation}:\n{str(e)}")

    def polar_2D_same(self):
        try:
            self.ui.fig2D.toggle_mode(False)
            self.ui.fig2D.plot_2D(self.model.h_plane2D, self.model.e_plane2D)
            self.ui.toolbar1.push_current()
        except Exception as e:
            QMessageBox.critical(self.ui, "Plot Error", f"Failed to switch to same-plot mode:\n{str(e)}")

    def polar_2D_split(self):
        try:
            self.ui.fig2D.toggle_mode(True)
            self.ui.fig2D.plot_2D(self.model.h_plane2D, self.model.e_plane2D)
            self.ui.toolbar1.push_current()
        except Exception as e:
            QMessageBox.critical(self.ui, "Plot Error", f"Failed to switch to split-plot mode:\n{str(e)}")

    def polar_3D(self):
        try:
            X, Y, Z = self.model.data_3D()
            if X is None or Y is None or Z is None:
                QMessageBox.warning(self.ui, "Data Warning", "3D data is not available. Please load a file first.")
                return
                
            self.ui.fig3D.plot_surface(X, Y, Z)
            self.ui.toolbar2.push_current()
        except AttributeError:
            QMessageBox.critical(self.ui, "Data Error", "Model data not available for 3D plotting. Please load a file first.")
        except Exception as e:
            QMessageBox.critical(self.ui, "3D Plot Error", f"Failed to create 3D plot:\n{str(e)}")

    def smooth_2D(self, number):
        try:
            if not hasattr(self.model, 'h_plane2D') or self.model.h_plane2D is None:
                QMessageBox.warning(self.ui, "Data Warning", "No 2D data available for smoothing. Please load a file first.")
                return
                
            self.model.smooth2D(number)
            self.ui.fig2D.plot_2D(self.model.h_plane2D, self.model.e_plane2D) 
            self.ui.toolbar1.push_current()  # Fixed: was toolbar2
            
            # Save smoothed state to history
            
            
        except ValueError as e:
            QMessageBox.critical(self.ui, "Smoothing Error", f"Invalid smoothing parameter:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self.ui, "Processing Error", f"Failed to apply 2D smoothing:\n{str(e)}")

    def smooth_3D(self,bool):
        
        if not hasattr(self.model, 'h_plane3D') or self.model.h_plane3D is None:
            QMessageBox.warning(self.ui, "Data Warning", "No 3D data available for smoothing. Please load a file first.")
            return
          
        self.model.smooth3D(bool)
        X, Y, Z = self.model.data_3D()
        self.ui.fig3D.plot_surface(X, Y, Z)
        self.ui.toolbar2.push_current()
        
        # Save smoothed state to history
        
            
        
    def color_2D(self):
        try:
            self.ui.pick_color_for()
            self.ui.fig2D.plot_2D(self.model.h_plane2D, self.model.e_plane2D)
            self.ui.toolbar1.push_current()
        except Exception as e:
            QMessageBox.critical(self.ui, "Color Error", f"Failed to change plot colors:\n{str(e)}")

    

    def save_project(self):
        try:
            file_path = self.ui.file_history("save")
            if not file_path:  # User cancelled save dialog
                return
                
            # Validate that we have data to save
            if not self.listHistory["h_plane2D"]:
                QMessageBox.warning(self.ui, "Save Warning", "No data available to save. Please load a file first.")
                return
                
            # Convert all numpy arrays to lists for JSON serialization
            serializable_history = {}
            for k, v in self.listHistory.items():
                serializable_history[k] = []
                for item in v:
                    try:
                        # Try to convert numpy array to list
                        serializable_history[k].append(item.tolist())
                    except (AttributeError, TypeError):
                        # If it's not a numpy array, keep as is
                        serializable_history[k].append(item)
            
            with open(file_path, 'w') as f:
                json.dump(serializable_history, f, indent=2)
                
            QMessageBox.information(self.ui, "Success", f"Project saved successfully to:\n{file_path}")
            
        except PermissionError:
            QMessageBox.critical(self.ui, "Permission Error", "You don't have permission to write to this location.")
        except OSError as e:
            QMessageBox.critical(self.ui, "File Error", f"Could not save file:\n{str(e)}")
        except json.JSONEncodeError as e:
            QMessageBox.critical(self.ui, "Data Error", f"Failed to serialize project data:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self.ui, "Save Error", f"Failed to save project:\n{str(e)}")

    def load_project(self):
        try:
            file_path = self.ui.file_history("open")
            if not file_path:  # User cancelled file dialog
                return
                
            # Check if file exists and is readable
            if not os.path.exists(file_path):
                QMessageBox.critical(self.ui, "File Error", f"File not found:\n{file_path}")
                return
                
            with open(file_path, 'r') as f:
                loaded_history = json.load(f)
            
            # Validate loaded data structure
            required_keys = ["h_plane2D", "e_plane2D", "h_plane3D", "e_plane3D", "e_color", "h_color"]
            if not all(key in loaded_history for key in required_keys):
                QMessageBox.critical(self.ui, "Data Error", "Invalid project file format. Missing required data fields.")
                return
                
            # Convert lists back to numpy arrays where appropriate
            for k, v in loaded_history.items():
                self.listHistory[k] = []
                for item in v:
                    try:
                        if k.endswith('plane2D') or k.endswith('plane3D'):
                            self.listHistory[k].append(np.array(item))
                        else:
                            self.listHistory[k].append(item)
                    except (ValueError, TypeError) as e:
                        QMessageBox.critical(self.ui, "Data Error", f"Corrupted data in project file for {k}:\n{str(e)}")
                        return
            
            self.index = len(self.listHistory["h_plane2D"]) - 1
            
            # Restore the latest state to the model/UI
            if self.index >= 0:
                self.model.h_plane2D = self.listHistory["h_plane2D"][self.index]
                self.model.e_plane2D = self.listHistory["e_plane2D"][self.index]
                self.model.h_plane3D = self.listHistory["h_plane3D"][self.index]
                self.model.e_plane3D = self.listHistory["e_plane3D"][self.index]
                self.ui.fig2D.color_h = self.listHistory["h_color"][self.index]
                self.ui.fig2D.color_e = self.listHistory["e_color"][self.index]
                
                
                # Redraw both plots
                self.ui.fig2D.plot_2D(self.model.h_plane2D, self.model.e_plane2D)
                X, Y, Z = self.model.data_3D()
                self.ui.fig3D.plot_surface(X, Y, Z)
                
            QMessageBox.information(self.ui, "Success", f"Project loaded successfully from:\n{file_path}")
            
        except FileNotFoundError:
            QMessageBox.critical(self.ui, "File Error", f"Project file not found:\n{file_path}")
        except PermissionError:
            QMessageBox.critical(self.ui, "Permission Error", "You don't have permission to read this file.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(self.ui, "Format Error", f"Invalid JSON format in project file:\n{str(e)}")
        except KeyError as e:
            QMessageBox.critical(self.ui, "Data Error", f"Missing required data in project file:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self.ui, "Load Error", f"Failed to load project:\n{str(e)}")
    #def online(self):
        