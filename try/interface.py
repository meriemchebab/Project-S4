import matplotlib as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
import sys
from PySide6.QtWidgets import QLabel ,QPushButton, QApplication,QMainWindow,QWidget,QHBoxLayout


class Myfig(FigureCanvas):
    def __init__(self,parent =None):
        self.fig= Figure(figsize=[2,4]) # here u create the plot figure
        self.ax = self.fig.add_subplot(111)
        
        super().__init__(self.fig)
        if parent :
            self.setParent(parent)
        
    def plot_data(self, x, y):
        """Method to plot data on the figure."""
        self.ax.clear()  # Clear previous plot
        self.ax.plot(x, y, label="Sample Data", color="b")
        self.ax.legend()
        self.draw() 


        
                   
class Button (QPushButton):
   
    def __init__(self,txt,parent =None):
        super().__init__(txt,parent)
        self.setCheckable(True)
        self.clicked.connect(self.fun)
    def fun(self,data):
         print("i azm a live",data)
   #signal ndiro hna 
    

    
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        main= QWidget()
        plot = Myfig(self)
        plot.plot_data([2,2,2,2,2] ,[3,4,5,7,8])

        
        button =Button( "meee",self)
        
       
        label = QLabel("hello world",self)
        layout = QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(label)
        layout.addWidget(plot)
        main.setLayout(layout)
        self.setCentralWidget(main)
    
app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()

