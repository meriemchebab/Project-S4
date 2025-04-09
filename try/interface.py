import matplotlib.pyplot as plt  # Correctly import pyplot
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
import sys
from PySide6.QtWidgets import QLabel ,QPushButton, QApplication,QMainWindow,QWidget,QHBoxLayout
import numpy as np

class Myfig(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=[4, 4])  # Create the plot figure
        super().__init__(self.fig)
        if parent:
            self.setParent(parent)

    def Polar_2d(self, data):
          # Draw the Plan H and Plan E
        self.fig.clear()
        half_length = len(data) // 2
        curve1 = np.array(data[:half_length])  # First half as Curve 1
        curve2 = np.array(data[half_length:])  # Second half as Curve 2
        theta = np.linspace(0, 2 * np.pi, half_length)  # Create angle values

        axes = self.fig.subplots(1, 2, subplot_kw={'projection': 'polar'})  # Fix subplots usage

        axes[0].plot(theta, curve1, label="Plan H", color='b')
        axes[0].set_title("Plan H")
        axes[0].legend()

        axes[1].plot(theta, curve2, label="Plan E", color='r')
        axes[1].set_title("Plan E")
        axes[1].legend()

        self.draw()


        
                   
class file_Button (QPushButton):
   
    def __init__(self,txt,parent =None):
        super().__init__(txt,parent)
        self.setCheckable(True)
        self.file =fileReader("try\courbe1.txt")
        
    
 
   #signal ndiro hna 
class fileReader():
    def __init__(self,file_name):
        self.file_name = file_name
    def read_file(self):
        degree = []
        with open(self.file_name, 'r') as file:
            for line in file:
                try:
                    lin = float(line)
                    degree.append(lin)
                except ValueError:
                    pass    
                except FileNotFoundError:
                    print(" damn girl you f up")
        return degree
    
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        main = QWidget()

        self.plot_widget = Myfig(self)  # Create an instance of Myfig
        Button = file_Button("open", self)
        layout = QHBoxLayout()
        layout.addWidget(Button)
        label = QLabel("hello world", self)

        layout.addWidget(Button)
        layout.addWidget(label)
        layout.addWidget(self.plot_widget)  # Add the plot widget to the layout
        main.setLayout(layout)
        self.setCentralWidget(main)
        Button.clicked.connect(lambda: self.plot_widget.Polar_2d(Button.file.read_file()))
    
    
app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()

