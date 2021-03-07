# animal.py by CoccaGuo at 2021/03/07 18:19
from with_time import WithTime
from vector3d import Position, Velocity
import uuid


class Animal(WithTime):
    def __init__(self, position, velocity, name="noname", age=0, weight=10, hp=100) -> None:
        self.position = position
        self.velocity = velocity
        self.name = name
        self.age = age
        self.weight = weight
        self.hp = hp
        self.uuid = uuid.uuid1()
    
    #animal can get hurt
    def hurt(self, hp_num):
        self.hp = self.hp - hp_num
    
    # animal can attack others
    def attack(self, other_animal, atk_num):
       other_animal.hurt(atk_num)

    # animal can get cured
    def cure(self, hp_num):
        self.hp = self.hp + hp_num

    # animal can move
    def move(self, displacement):
        self.position.add(displacement)
    
    # because implemented WithTime
    def next_tick(self):
        
        #deal with moving
        self.move(self.velocity)
