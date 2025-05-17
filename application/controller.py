from logic import Model
from UI_file import Window
from PySide6.QtCore import QObject

class Controler(QObject):
    def __init__(self  ,  parent = None):
        super().__init__(parent)
        self.model=Model(self)
        self.ui = Window(self)
        self.mode = None
        self.listHistory = {
                 "h_plane":[],
                "e_plane":[],
            }
        self.index = -1
        # the signals and slots 

        self.ui.main.button.clicked.connect(self.read)

        
#reading a file

    def read(self):
            
            file_name = self.ui.open_file()
            self.model.read_file(file_name)
            
            # this is the history i take a reference of the data so i can go back to it 
            Hdata = self.model.h_plane
            Edata = self.model.e_plane

            self.listHistory["h_plane"].append(Hdata)
            self.listHistory["e_plane"].append(Edata)
            self.index +=1
            # when the previos button clik
            # go for this
    def can_goBack(self):
            if self.index > 0 :
                  return True
            else :
                return False

    def can_goForth(self):
          return self.index < len(self.listHistory["h_plane"])-1
             
            #index = length(self.listHistory["h_plane"]) - 1
    def GoBack(self):
          if self.can_goBack():
            self.index -=1
            self.model.h_plane = self.listHistory["h_plane"][self.index]
            self.model.e_plane = self.listHistory["e_plane"][self.index]
            self.model.clear_data()
# forth buton 
    def GoForth(self):
         if  self.can_goForth():
            self.index +=1
            self.model.h_plane = self.listHistory["h_plane"][self.index]
            self.model.e_plane = self.listHistory["e_plane"][self.index]          
            self.model.clear_data()
    def polar_2D_same(self):
         self.ui.fig2D.clf()
         self.mode = 1
         self.ui.fig2D.update_ax2(self.mode)
         self.ui.plot_2D(self.mode)
    def polar_2D_split(self):
        self.ui.fig2D.figure.clf()
        self.mode = 2
        self.ui.fig2D.update_ax2(self.mode)
        self.ui.plot_2D(self.model.h_plane,self.model.e_plane ,self.mode) 
    def polar_3D(self):
      self.ui.fig3D.figure.clf()
      self.ui.fig3D.setupAX3()
      self.ui.plot_3D()
    def normal(self):
         


         
         
# this for the smooth set the max to be dinamic
    #max_window = len(self.h_plane) // 5
    #if max_window % 2 == 0:
       # max_window -= 1
    #slider.setRange(5, max_window)
     
        

