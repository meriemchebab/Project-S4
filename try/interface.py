import matplotlib.pyplot as plt  # Correctly import pyplot
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
import sys
from PySide6.QtWidgets import QLabel ,QPushButton, QApplication,QMainWindow,QWidget,QHBoxLayout,QFileDialog
import numpy as np

class Myfig(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=[12, 7])  # Create the plot figure , here you will see the plot 
        super().__init__(self.fig)
        if parent:
            self.setParent(parent)
    
class button(QPushButton):
    def __init__(self, txt, parent=None):
        super().__init__(txt, parent)  
        self.txt = txt

class Window(QMainWindow):#main window to see the app 
    def __init__(self):
        super().__init__()
        main = QWidget()

        self.plot_widget = Myfig(self)  # Create an instance of Myfig
        self.saveButton = button("open", self)
        self.plot2D = button("plot", self)

        layout = QHBoxLayout()
        layout.addWidget(self.saveButton)
        layout.addWidget(self.plot2D)
        layout.addWidget(self.plot_widget)  # Add the plot widget to the layout
        main.setLayout(layout)
        self.setCentralWidget(main)

        # when open file button:
        self.saveButton.clicked.connect(self.read_file)
        # plot the data
        self.plot2D.clicked.connect(self.plot_2D)

        self.data = []  # Store the data for plotting

    def read_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)  # on file each time
        dialog.setNameFilter("Text Files (*.txt);;atn files (*.atn);; csv (*.csv)")  # 🧽 Filters
        if dialog.exec():
            file_name = dialog.selectedFiles()[0]  # Get the selected file

            degree = []
            try:
                with open(file_name, 'r') as file:
                    for line in file:
                        try:
                            lin = float(line)
                            degree.append(lin)
                        except :
                            pass
                self.data = degree  # Store the data for plotting
            except FileNotFoundError:
                print("File not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
            

    def plot_2D(self):
        if not self.data or len(self.data) < 720:
            print("Insufficient data to plot.")
            return

        
        h_plane_db = np.array(self.data[:360])
        e_plane_db = np.array(self.data[360:720])

        # Create angle array
        phi = np.radians(np.arange(360))  

        
        self.plot_widget.fig.clear()

        # Create polar subplots
        fig_polar, axes = self.plot_widget.fig.subplots(1, 2, subplot_kw={'projection': 'polar'})

        # H-plane plot
        axes[0].plot(phi, h_plane_db, label='H-plane', color='blue')
        axes[0].set_title('H-plane Pattern (dB)')
        axes[0].legend()

        # E-plane plot
        axes[1].plot(phi, e_plane_db, label='E-plane', color='red')
        axes[1].set_title('E-plane Pattern (dB)')
        axes[1].legend()

        # Set the title and layout
        fig_polar.suptitle('2D Radiation Patterns (Smoothed in dB)')
        fig_polar.tight_layout()

        # Draw the updated figure on the canvas
        self.plot_widget.draw()
        
app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()

