import matplotlib as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
import sys
from PySide6.QtWidgets import QLabel ,QPushButton, QApplication,QMainWindow,QWidget,QHBoxLayout


class Myfig(FigureCanvas):
    def __init__(self,parent =None):
        self.fig= Figure(figsize=[4,4]) # here u create the plot figure
        
        
        super().__init__(self.fig)
        if parent :
            self.setParent(parent)
        
    


        
                   
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
        

        
        button =Button( "meee",self)
        
       
        label = QLabel("hello world",self)
        layout = QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(label)
        #layout.addWidget(plot)
        main.setLayout(layout)
        self.setCentralWidget(main)
    
app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()

