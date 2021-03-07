# position.py by CoccaGuo at 2021/03/07 18:19
# (x,y,z) also used as displacement
class Vector3d:  
    def __init__(self, x, y, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z
    

    def add(self, pos):
        self.x = self.x + pos.x
        self.y = self.y + pos.y
        self.z = self.z + pos.z
    
    def string(self):
        return "x: {:.2f} y: {:.2f} z: {:.2f}".format(self.x, self.y, self.z)


class Position(Vector3d):
    pass

class Velocity(Vector3d):
    pass

# simple to write
class V(Vector3d):
    pass