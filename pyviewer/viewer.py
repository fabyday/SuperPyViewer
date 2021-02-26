
import sys 
import numpy as np 
import logging 
import igl

from OpenGL.GL import * 

from OpenGL.GLU import *

# import viewcontrolobj as vco




logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Viewer Logger")

from pyviewer import datacontainer as dc



from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from pyviewer import ui
from pyviewer import viewcontrolobj as vco 


from pyviewer import controller, data_model

QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)

app = QApplication(sys.argv)

class CustomViewer(QMainWindow):
    def __init__(self, title, width, height):

        super().__init__()
        self.resize(width, height)
        # self.layout = BorderLayout()
        self.windows = []
        self.world = dc.WorldContainer()
        # self.initUI()

    def add_window(self, window, isdock=True, name="", allowed_area=Qt.AllDockWidgetAreas, central=False):
        """
            window is QT Window Object. and window_object has lisener
        """
        print("centerla" , central)
        if isdock and not central : 
            dock = QDockWidget(name, self)
            dock.setFloating(False)
            self.windows.append(dock)
            dock.setAllowedAreas(allowed_area)
            dock.setWidget(window)
            dock.widget().setMaximumSize(dock.widget().minimumSize())

            # self.addDockWidget(Qt.RightDockWidgetArea, dock)
            self.addDockWidget(allowed_area, dock)
            
        elif  central:

            self.setCentralWidget(window)
            
            


    def initUI(self):
        self.menu = ui.UIMenuBar(self)
        self.menu.initUI()
        self.Inspector = ui.InspectorUI(self)    
        self.Inspector.initUI()
        


    def set_data(self, V, F):
        # self.data.append( (V,F))
        self.world.add_data(dc.DataContainer(V, F))
        
    def compile(self):
        self._initialize_mainview()

        self.initUI()


    def _initialize_mainview(self):
        win = vco.Window("tit")
        win.set_world(self.world)
        self.add_window(win, isdock=True, name=win.name, central=True)
        
    

    def run(self):

        self.show()
    

    # def mouseMoveEvent(self, pos):
    #     print(pos.x(), pos.y(), "pos is :")







if __name__ == "__main__":
    V, F = igl.read_triangle_mesh("pyviewer/cube.obj")
    # V, F = igl.read_triangle_mesh("pyviewer/cube.ply")
    # a = Viewer("title", 800, 900)
    # a.set_data(V,F)
    # a.add_mouse_down_callback(test_mouse)
    # a.add_mouse_up_callback(test_mouse_pop)
    # a.add_mouse_motion_callback(test_mouse_motion)
    # a.launch()
if __name__ == '__main__':
    
    window = CustomViewer("hee", 800,900)
    window.set_data(V,F)
    window.compile()
    window.run()

    sys.exit(app.exec_())