# position.py by CoccaGuo at 2021/03/07 18:19
# (x,y,z) also used as displacement

from math import sqrt

class Vector3d:  
    def __init__(self, x, y, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z
    

    def add(self, pos):
        x = self.x + pos.x
        y = self.y + pos.y
        z = self.z + pos.z
        return V(x, y, z)


    def minus(self, pos):
        x = self.x - pos.x
        y = self.y - pos.y
        z = self.z - pos.z
        return V(x, y, z)
    
    
    def mul(self, number):
        x = self.x * number
        y = self.y * number
        z = self.z * number
        return V(x, y, z)

    
    def normalize(self):
        length = sqrt(self.x**2+self.y**2+self.z**2)
        if length == 0:
            return V(0, 0, 0)
        return V(self.x/length, self.y/length, self.z/length)

    
    def distance(self, pos):
        return sqrt((self.x-pos.x)**2+(self.y-pos.y)**2+(self.z-pos.z)**2)
        
    
    def string(self):
        return "x: {:.2f} y: {:.2f} z: {:.2f}".format(self.x, self.y, self.z)


class Position(Vector3d):
    pass

class Velocity(Vector3d):
    pass

# simple to write
class V(Vector3d):
    pass