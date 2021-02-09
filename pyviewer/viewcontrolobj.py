import numpy as np 
from OpenGL.GL import * 
from OpenGL.GLU import *

import numpy as np 

# NEED GL BUILDER 
# import datacontainer
from pyviewer import datacontainer
from pyviewer import AABB


class Light():
    def __init__(self):
        self.position = [0.0, 0.0, 1.0, 0.0]
        self.direcion = [0., 0., -1.]
        self.set_ambient([1.0, 1.0, 1.0, 0.0])
        self.set_ambient([0.0, 0.0, 0.0, 0.0])
        self.set_diffuse([1.0, 1.0, 1.0, 0.0])
        self.set_specular([1.0, 1.0, 1.0, 0.0])

        self.set_coeff()

    

    def set_coeff(self, constant =1.0, linear = 0.09, quadratic = 0.032):
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic


    def set_ambient(self, ambient):
        self.ambient = ambient
        return self 


    def set_diffuse(self, diffuse):
        self.diffuse = diffuse
        return self

    def set_specular(self, specular):
        self.specular = specular
        return self
    
    def initialize(self):
        glClearColor(0.,0.,0.,0.)
        glClearDepth(1.0)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)
        glEnable(GL_NORMALIZE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.specular)
        glLightfv(GL_LIGHT0, GL_POSITION, self.position)

    
    def __call__(self):
        pass

class Material():
    def __init__(self):
        # self.set_ambient([0.2, 0.2 , 0.2 , 0.0])
        self.set_ambient([1., 1. , 1. , 0.0])
        self.set_diffuse([1. , 1, 1., 0.0])
        self.set_specular([0.2, 0.2, 0.2, 0.0])
        self.set_emission([1.0, 0.0, 1.0, 0.0])
        self.set_shininess([1.0])

    def set_ambient(self, ambient):
        self.ambient = ambient
        return self
    def set_diffuse(self, diffuse):
        self.diffuse = diffuse
        return self
    def set_specular(self, specular):
        self.specular = specular
        return self

    def set_shininess(self, shininess):
        self.shininess = shininess
        return self
    def set_emission(self, emission):
        self.emission = emission
    

    def initialize(self):
        glEnable(GL_COLOR_MATERIAL)

    def __call__(self):
        # glEnable(GL_COLOR_MATERIAL)
        
        # disable it. for using glMatrialfv function. not glcolor
        # see also https://www.khronos.org/opengl/wiki/File:Opengl_lighting_flowchart.png
        

        # glDisable(GL_COLOR_MATERIAL)        
        # glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.ambient + self.diffuse)
        glEnable(GL_COLOR_MATERIAL)
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.shininess)
        glMaterialfv(GL_FRONT, GL_EMISSION, self.emission)
        # glEnable(GL_COLOR_MATERIAL)

        #anti aliasing
        # glEnable(GL_BLEND);
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
 



        # glEnable(GL_LINE_SMOOTH)
        # glEnable(GL_POINT_SMOOTH)

        

class VCOCollection():
    """
        View Controll Object Collection Class 


        Controll Cam_lists, Viewer State
    """
    def __init__(self):
        self.world = []
        self.windows =[]
        # self.
    
    def add_window(self):
        pass
    
    def read_default_yaml(self, file_name):
        pass

class LayoutOptions():
    def __init__(self):
        pass

    def set_layout(self):
        pass
class GL_Options():
    def __init__(self):
        pass
    

class RootWindow():
    def __init__(self, x, y, width, height, title = None):
        if title == None : 
            title = "No Title"
        self.title = title
        self.set_layout(1,1)
        self.vco = VCOCollection()
        self.child_group = [[]]
        self.gui = []

        self.x = x 
        self.y = y
        self.width = width 
        self.hegiht = height
        
        
        
        
        
    def _set_xywh(self, x, y, width, height):
        cond_function = lambda x : x > 0
        def _set_attribute(x, func):
            if func(x):
                return x
        self.width =  _set_attribute(width, cond_function )
        self.height = _set_attribute(height, cond_function )
        self.x = _set_attribute(x, cond_function )
        self.y = _set_attribute(y, cond_function )

    def reshape(x, y, width, height):
        
        self._set_attribute(x,y,width,height)
        child_width = width / self.cols
        child_height = height / self.rows

        for group_idx, group in enumerate(self.child_group):
            map_col = (group_idx) % self.cols # 0 ~ n - 1 
            map_row = (group_idx) // self.rows  # 0 ~ n - 1
            for window in group :
                window.reshape(x + map_col * child_width, y + map_row * child_height, child_width, child_height)
    

    def draw(self):
        pass

        



    def set_layout(self, rows, cols):
        self.rows = self.rows
        self.cols = self.cols
    

from PyQt5.QtWidgets import (QApplication, QMainWindow, OpenGLQT, QTextEdit, QDockWidget, QListWidget)
from PyQt5.QtCore import Qt


class Window():
    """
        Class Window Draw World. 
    """
    WIN_NUM = 0
    def __init__(self, viewer_name = None):
        if viewer_name == None : 
            viewer_name = "NoNameW_" +str(Window.WIN_NUM)
            Window.WIN_NUM += 1
        self.name = viewer_name
        self.camera = Camera()
        self.x = 0
        self.y = 0
        self.width = -1.
        self.height = -1.

    def reshape(self,x,y, w, h):
        self._set_xywh( x, y, w, h)
        
    def get_ray(self, x, y):
        return self.camera.get_ray(x,y, self.width, self.height)

    def _set_xywh(self, x, y, width, height):
        # glViewport(x,y,width, height)
        
        cond_function = lambda x : x > 0
        def _set_attribute(x, func):
            if func(x):
                return x
        width =  _set_attribute(width, cond_function )
        height = _set_attribute(height, cond_function )
        self.factor_width = 1 if self.width == -1 else width/self.width
        self.factor_height = 1 if self.width == -1 else width/self.width
        self.width =  _set_attribute(width, cond_function )
        self.height = _set_attribute(height, cond_function )
        self.x = _set_attribute(x, cond_function )
        self.y = _set_attribute(y, cond_function )

    def draw(self, world):
        # glViewport(self.x, self.y, self.width, self.height)
        
        world.light_initialize()
        self.camera(self.factor_width, self.factor_height)
        world.world_draw()
        
        

class Camera():
    
    CAM_NUM = 0
    PERSPECTIVE_MODE = "perspect"
    ORTHGONAL_MODE = "ortho"
    def __init__(self):
        self.default_cam_pos = self.cam_pos = [0.,0.,1.]
        self.default_cam_direct = self.cam_direct = [0.,0.,-1.]
        self.default_cam_normal_direction = self.cam_normal_direction = [0.,1.,0.]
        self.mode = Camera.ORTHGONAL_MODE

        # example
        self.near = 0
        self.far = 0


    def set_name(self, name=None):
        if name == None : 
            name = "NoNameCam_"+str(Camera.CAM_NUM)
            Camera.CAM_NUM += 1
        self.name = name

    def set_campos(self, x, y, z):
        self.cam_pos[0] = x
        self.cam_pos[1] = y
        self.cam_pos[2] = z

    def update_campos(self, delta_x, delta_y, delta_z):
        self.cam_pos[0] += delta_x
        self.cam_pos[1] += delta_y
        self.cam_pos[2] += delta_z
        return self
    
    def rotate(self, angle, axis):
        
        return self
    
    def set_direction(self, x, y, z):
        if not [(self.cam_pos[x] + self.cam_pos[y] +self.cam_pos[z] - x - y - z) == 0 ]:
            self.cam_direct[x] = x 
            self.cam_direct[y] = y
            self.cam_direct[z] = z

    def __call__(self, w_factor = 1., h_factor = 1.):
        #Add transform after....
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.w_factor = w_factor
        self.h_factor = h_factor
        # gluPerspective(45, (1/ 2), 0.1, 50.)

        glOrtho(-1*w_factor, 1*w_factor, -1*h_factor, 1*h_factor, -2, 2)
        # glTranslatef(*self.cam_pos)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*self.cam_pos, *self.cam_direct, *self.cam_normal_direction)

        # return self.cam_pos, self.cam_direct, cam_normal_direction

    def get_ray(self, x, y, res_w, res_h):
        """
            INPUT
                viewport coordinate x, y 
            Return
                world coordinate (x,y,z) ray object
        """
        # inverse processing. display coord -> NDC coord
        ndc_x = ((x * 2 )/ res_w - 1*self.w_factor)
        ndc_y = -((y * 2 ) / res_h - 1*self.h_factor)
        print("view x y : ", x,y)
        print("w_f {} w_h".format(self.w_factor,self.h_factor))
        print(res_w, res_h)
        print("ndc_coord x : {} y : {}".format(ndc_x, ndc_y))
        z = 1
        # z = -1
        # NDC coord -> projection 
        
        # projection -> cam coord
        Lookatcam = np.eye(4,4)
        array = (GLfloat *16)()
        
        glGetFloat(GL_PROJECTION_MATRIX, array)
        toeye = np.array(array).reshape(4,4)
        toeye = np.linalg.inv(toeye.T)
        array2 = (GLfloat *16)()

        glGetFloat(GL_MODELVIEW_MATRIX, array2)
        toworld = np.array(array2).reshape(4,4)
        toworld = np.linalg.inv(toworld.T)


        Lookatcam[0, :-1] = np.cross( np.array(self.cam_direct), np.array(self.cam_normal_direction))
        # Lookatcam[0, :-1] = np.cross( np.array(self.cam_normal_direction), np.array(self.cam_direct) )
        Lookatcam[1, :-1] = np.array(self.cam_normal_direction)
        Lookatcam[2, :-1] = np.array(self.cam_direct) 
        # print(Lookatcam, "look_rot")

        Lookatpos = np.eye(4,4)
        Lookatpos[:-1, -1] = - np.array(self.cam_pos)

        # print(Lookatpos, "lookpos")

        Looks = Lookatcam.dot(Lookatpos)
        inv_Lat = np.linalg.inv(Looks)
        
        # print(Looks, "looks")
        # print(inv_Lat, "inv_looks")

        # direction = inv_Lat.dot(np.array([ndc_x, ndc_y, z, 0]))
        direction = inv_Lat.dot(np.array([0, 0, z, 0]))
        # pos = inv_Lat.dot(np.array([0.0, 0.0, 0.0, 1.0 ]))
        pos = inv_Lat.dot(np.array([ndc_x, ndc_y, 0.0, 1.0 ]))
        
        # TMP TODO
        direction =toworld.dot(toeye.dot(np.array([0, 0, z, 0])))
        # pos =toworld.dot(toeye.dot(np.array([ndc_x,ndc_y,0.0, 1])))
        pos =toworld.dot(toeye.dot(np.array([ndc_x,ndc_y,0.0, 1.])))
        

        reval = AABB.Ray()
        reval.set_pos(pos[:3])
        # import copy
        # ss = copy.deepcopy(direction[:3])
        # ss[-1] = pos[:3][-1]
        # reval.set_pos(ss)

        reval.set_direction(direction[:3])
        print("ray val", reval)
        return reval
        



if __name__ == "__main__":
    testcam = Camera()
    reval = testcam.get_ray(0,0, 300, 400)
    print(reval)
    