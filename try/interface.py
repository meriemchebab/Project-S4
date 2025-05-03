from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import sys
from PySide6.QtWidgets import (QPushButton, QApplication, QMainWindow, 
                              QWidget, QVBoxLayout, QFileDialog, 
                              QRadioButton, QHBoxLayout,QSlider)
import numpy as np
from PySide6.QtCore import Qt
class Myfig(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=[12, 7])
        super().__init__(self.fig)
        if parent:
            self.setParent(parent)
        # Initialize axes as None (we'll create them when needed)
        self.ax1 = None
        self.ax2 = None
    
class Button(QPushButton):
    def __init__(self, txt, parent=None):
        super().__init__(txt, parent)  
        self.txt = txt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        main = QWidget()

        self.plot_widget = Myfig(self)
        self.readButton = Button("open", self)
        self.plot2D = Button("plot", self)
        self.normal = QRadioButton("normelize", self)
        
        self.toolbar = NavigationToolbar(self.plot_widget, self)
        self.slider = QSlider()
        self.slider.setMaximum(6)
        self.slider.setMinimum(1)
        self.slider.setOrientation(Qt.Horizontal) 

        Button_row = QHBoxLayout()
        Button_row.addWidget(self.readButton)
        Button_row.addWidget(self.plot2D)
        Button_row.addWidget(self.normal)

        layout = QVBoxLayout()
        layout.addLayout(Button_row)
        layout.addWidget(self.slider)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.plot_widget, stretch=1)
        main.setLayout(layout)
        self.setCentralWidget(main)

        self.readButton.clicked.connect(self.read_file)
        self.plot2D.clicked.connect(self.plot_2D)
        self.normal.toggled.connect(self.plot_2D)

        self.data = []
        self.h_plane = []
        self.e_plane = []

    def read_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("Text Files (*.txt);;atn files (*.atn);; csv (*.csv)")
        if dialog.exec():
            file_name = dialog.selectedFiles()[0]
            
            self.h_plane = []
            self.e_plane = []

            reading_started = False
            reading_h_plane = True

            with open(file_name, 'r') as file:
                for line in file:
                    line = line.strip()
                    
                    if not line:
                        continue

                    try:
                        value = float(line)
                        reading_started = True

                        if reading_h_plane:
                            self.h_plane.append(value)
                        else:
                            self.e_plane.append(value)

                    except ValueError:
                        if reading_started:
                            reading_h_plane = False
                        continue

    def plot_2D(self):
        if not (self.h_plane or self.e_plane):
            print("Insufficient data to plot.")
            return
        
        h_plane_db = np.array(self.h_plane)
        e_plane_db = np.array(self.e_plane)
        
        if self.normal.isChecked()  :
            if self.h_plane :
                h_plane_db = self.normelize(h_plane_db)
            if self.e_plane :
                e_plane_db = self.normelize(e_plane_db)

        phi_h = np.radians(np.arange(len(h_plane_db)))  
        phi_e = np.radians(np.arange(len(e_plane_db)))
        
        # Instead of clf(), clear the existing axes if they exist
        if self.plot_widget.ax1 is not None:
            self.plot_widget.ax1.clear()
        else:
            self.plot_widget.ax1 = self.plot_widget.fig.add_subplot(1, 2, 1, projection='polar')
        
        if self.plot_widget.ax2 is not None:
            self.plot_widget.ax2.clear()
        else:
            self.plot_widget.ax2 = self.plot_widget.fig.add_subplot(1, 2, 2, projection='polar')

        # Plot H-plane
        self.plot_widget.ax1.plot(phi_h, h_plane_db, label='H-plane', color='blue')
        self.plot_widget.ax1.set_title('H-plane Pattern (dB)')
        self.plot_widget.ax1.set_theta_zero_location('N')
        self.plot_widget.ax1.set_theta_direction(-1)
        self.plot_widget.ax1.legend()

        # Plot E-plane
        self.plot_widget.ax2.plot(phi_e, e_plane_db, label='E-plane', color='red')
        self.plot_widget.ax2.set_title('E-plane Pattern (dB)')
        self.plot_widget.ax2.legend()

        # Redraw the canvas
        self.plot_widget.draw()
        
        # Push the current view to the navigation stack
        self.toolbar.push_current()

    def normelize(self, dataN):
        data = dataN - np.max(dataN)
        return data

def load_stylesheet(app, qss_file_path):
    
    try:
        with open(qss_file_path, "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print(f"Stylesheet file not found: {qss_file_path}")
    except Exception as e:
        print(f"An error occurred while loading the stylesheet: {e}")

# Main application setup
app = QApplication(sys.argv)


qss_file_path = r"C:\Users\hp\Desktop\Project\Project-S4\try\style.qss"

load_stylesheet(app, qss_file_path)

window = Window()
window.show()
app.exec()