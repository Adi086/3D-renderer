import pygame
import numpy as np
from pygame.locals import *
import math

#Initializing Pygame
pygame.init()

#screen
WIDTH,HEIGHT = 1000,700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
ui = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("3D Renderer")
clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)
GREY=(31, 31, 31)

#VARIABLES
poitnSize=3
lineThinkness= 1
zoomValue=1
O_x=WIDTH/2
O_y=HEIGHT/2
O_z=100

#FONT
font=pygame.font.Font("PIXELLARI.ttf",10)

running=True

class globalObject:
    drag_x = 0
    drag_y = 0
    dragging = False
    offset_x = 0
    offset_y = 0
    
    @classmethod
    def drag(cls, event):
        """Handles dragging of all objects globally."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                cls.dragging = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                cls.offset_x = cls.drag_x - mouse_x
                cls.offset_y = cls.drag_y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            cls.dragging = False

        elif event.type == pygame.MOUSEMOTION and cls.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cls.drag_x = mouse_x + cls.offset_x
            cls.drag_y = mouse_y + cls.offset_y
    
    @classmethod
    def zoom(cls,event):
        global zoomValue
        if event.type == pygame.MOUSEWHEEL:
            zoomValue+=event.y/70

class Origin(globalObject):
    def __init__(self):
        self.x=O_x
        self.y=O_y
        self.z = O_z
    
    def pos2D(self):
        return pygame.Vector2(self.x + self.drag_x,self.y + self.drag_y)

    def draw(self,surface):
        pygame.draw.circle(surface, RED,(self.pos2D().x,self.pos2D().y),poitnSize)

class AxisLineY(globalObject):
    def __init__(self,a,b):
        self.a=a
        self.b=b
    
    def pos3D_start(self):
        return pygame.Vector3(self.a)
    def pos3D_end(self):
        return pygame.Vector3(self.b)
    
    def pos2D_start(self):
        return pygame.Vector2((self.a[0] + self.drag_x,self.a[1] +self.drag_y))
    def pos2D_end(self):
        return pygame.Vector2((self.b[0] + self.drag_x,self.b[1] + self.drag_y))
    
    def draw(self,surface,color):
        return pygame.draw.line(surface, color, self.pos2D_start()-(0,self.drag_y),self.pos2D_end()-(0,self.drag_y),lineThinkness)
    
class AxisLineX(globalObject):
    def __init__(self,a,b):
        self.a=a
        self.b=b
    
    def pos3D_start(self):
        return pygame.Vector3(self.a)
    def pos3D_end(self):
        return pygame.Vector3(self.b)
    
    def pos2D_start(self):
        return pygame.Vector2((self.a[0] + self.drag_x,self.a[1] +self.drag_y))
    def pos2D_end(self):
        return pygame.Vector2((self.b[0] + self.drag_x,self.b[1] + self.drag_y))
    
    def draw(self,surface,color):
        return pygame.draw.line(surface, color, self.pos2D_start()-(self.drag_x,0),self.pos2D_end()-(self.drag_x,0),lineThinkness)

class Line(globalObject):
    def __init__(self,a,b):
        self.a=a
        self.b=b
    
    def pos3D_start(self):
        return pygame.Vector3(self.a)
    def pos3D_end(self):
        return pygame.Vector3(self.b)
    
    def pos2D_start(self):
        return pygame.Vector2((self.a[0] + self.drag_x,self.a[1] +self.drag_y))
    def pos2D_end(self):
        return pygame.Vector2((self.b[0] + self.drag_x,self.b[1] + self.drag_y))
    def pos2D_start_perspective(self):
        return pygame.Vector2((self.a[0]*700/(self.a[2]+700),self.a[1]*700/(self.a[2]+700)))*zoomValue
    def pos2D_end_perspective(self):
        return pygame.Vector2((self.b[0]*700/(self.b[2]+700),self.b[1]*700/(self.b[2]+700)))*zoomValue

    def draw(self,surface,color):
        return pygame.draw.line(surface, color, self.pos2D_start_perspective()+(self.drag_x,self.drag_y),self.pos2D_end_perspective()+(self.drag_x,self.drag_y),lineThinkness)

class Cube(globalObject):
    def __init__(self,a,sideLength):
        self.a=a
        self.side = sideLength

    def center(self):
        return pygame.Vector3(self.a)  

    def draw(self,surface,color):
        s1=Line((self.center()+(self.side/2,self.side/2,self.side/2)),(self.center()+(-self.side/2,self.side/2,self.side/2)))
        s2=Line((self.center()+(self.side/2,self.side/2,self.side/2)),(self.center()+(self.side/2,-self.side/2,self.side/2)))
        s3=Line((self.center()+(self.side/2,self.side/2,self.side/2)),(self.center()+(self.side/2,self.side/2,-self.side/2)))
        s4=Line((self.center()+(-self.side/2,-self.side/2,-self.side/2)),(self.center()+(self.side/2,-self.side/2,-self.side/2)))
        s5=Line((self.center()+(-self.side/2,-self.side/2,-self.side/2)),(self.center()+(-self.side/2,self.side/2,-self.side/2)))
        s6=Line((self.center()+(-self.side/2,-self.side/2,-self.side/2)),(self.center()+(-self.side/2,-self.side/2,self.side/2)))
        s6=Line((self.center()+(-self.side/2,-self.side/2,-self.side/2)),(self.center()+(-self.side/2,-self.side/2,self.side/2)))
        s7=Line((self.center()+(-self.side/2,self.side/2,self.side/2)),(self.center()+(-self.side/2,-self.side/2,self.side/2)))
        s8=Line((self.center()+(self.side/2,-self.side/2,self.side/2)),(self.center()+(-self.side/2,-self.side/2,self.side/2)))
        s9=Line((self.center()+(self.side/2,self.side/2,-self.side/2)),(self.center()+(-self.side/2,self.side/2,-self.side/2)))
        s10=Line((self.center()+(-self.side/2,self.side/2,self.side/2)),(self.center()+(-self.side/2,self.side/2,-self.side/2)))
        s11=Line((self.center()+(self.side/2,-self.side/2,self.side/2)),(self.center()+(self.side/2,-self.side/2,-self.side/2)))
        s12=Line((self.center()+(self.side/2,self.side/2,-self.side/2)),(self.center()+(self.side/2,-self.side/2,-self.side/2)))
        return s1.draw(surface,color),s2.draw(surface,color),s3.draw(surface,color),s4.draw(surface,color),s5.draw(surface,color),s6.draw(surface,color),s7.draw(surface,color),s8.draw(surface,color),s9.draw(surface,color),s10.draw(surface,color),s11.draw(surface,color),s12.draw(surface,color)
        
class Button:
    def __init__(self,x,y,xlen,ylen,text,textcolor):
        self.x=x
        self.y=y
        self.xlen=xlen
        self.ylen=ylen
        self.text=text
        self.textcolor=textcolor
        self.txtsurf=font.render(text,True,textcolor)
    
    def create(self,surface,color,width,border_Radius):
        return pygame.draw.rect(surface,color,(self.x,self.y,self.xlen,self.ylen),width,border_Radius),ui.blit(self.txtsurf,(self.x+self.xlen//4,self.y+self.ylen//3))

class txtDisplay:
    def __init__(self,text,color):
        self.text=text
        self.color=color
        self.txt= font.render(text,True,color)
    
    def write(self):
        return ui.blit(self.txt,(20 - self.txt.get_width() // 2, 15 - self.txt.get_height() // 2))

origin = Origin()
yaxis=AxisLineY((O_x,0,100),(O_x,2*O_y,100))
xaxis=AxisLineX((0,O_y,100),(2*O_x,O_y,100))
#line = Line((300,200,500),(500,400,100))
cube = Cube((500,200,100),200)
button=Button(200,300,60,60,"ABCD",WHITE)


def reference():
    origin.draw(screen)
    yaxis.draw(screen,GREY)
    xaxis.draw(screen,GREY)
    #line.draw(screen,WHITE)

while (running):
    screen.fill(BLACK)
    ui.fill((0,0,0,0))
    reference()

    
    
    cube.draw(screen,GREEN)
    button.create(ui,WHITE,1,5)

   # pygame.draw.line(screen,GREEN,(510,200),(900,300),1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    
        globalObject.drag(event)
        globalObject.zoom(event)
    pygame.display.flip()

pygame.quit()