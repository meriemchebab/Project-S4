  # Correctly import pyplot
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import sys
from PySide6.QtWidgets import QPushButton, QApplication,QMainWindow,QWidget,QVBoxLayout,QFileDialog,QRadioButton,QHBoxLayout
 
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
        self.readButton = button("open", self)
        self.plot2D = button("plot", self)
        self.normal = QRadioButton("normelize",self)
        
        self.toolbar = NavigationToolbar(self.plot_widget, self)
        

        
        
        button_row = QHBoxLayout()
        button_row.addWidget(self.readButton)
        button_row.addWidget(self.plot2D)
        button_row.addWidget(self.normal)

        

        layout = QVBoxLayout()
        layout.addLayout(button_row)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.plot_widget, stretch=1)
          # Add the plot widget to the layout
        main.setLayout(layout)
        self.setCentralWidget(main)

        # when open file button:
        self.readButton.clicked.connect(self.read_file)
        # plot the data
        self.plot2D.clicked.connect(self.plot_2D)
        # the offset 
        
        self.normal.toggled.connect(self.plot_2D)

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
        if not self.data :
            print("Insufficient data to plot.")
            return
        
        
        h_plane_db = np.array(self.data[:360])
        e_plane_db = np.array(self.data[360:720])
        
        # do the offset if the smooth button is clicked
        if self.normal.isChecked():
            h_plane_db = self.normelize(h_plane_db)
            e_plane_db = self.normelize(e_plane_db)

          
        # Create angle array
        phi = np.radians(np.arange(360))  

        
        self.plot_widget.fig.clf() #this clear all the subplots 
        

        # Create polar subplots
        ax1 = self.plot_widget.fig.add_subplot(1, 2, 1, projection='polar')
        ax2 = self.plot_widget.fig.add_subplot(1, 2, 2, projection='polar')

        # 3. Plot H-plane
        ax1.plot(phi, h_plane_db, label='H-plane', color='blue')
        ax1.set_title('H-plane Pattern (dB)')
        ax1.legend()

        # 4. Plot E-plane
        ax2.plot(phi, e_plane_db, label='E-plane', color='red')
        ax2.set_title('E-plane Pattern (dB)')
        ax2.legend()

        # 5. Redraw the canvas
        self.plot_widget.draw()
    def normelize(self, dataN):

        data  = dataN - np.max(dataN)
        return data
        
app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()

